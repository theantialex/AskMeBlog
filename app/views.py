from django.db.models import F
from django.http import JsonResponse
from django.shortcuts import render
from django.core.paginator import Paginator
from django.views.decorators.http import require_POST

from .models import *
from django.contrib.auth.decorators import login_required
from .forms import *
from django.contrib import auth
from django.shortcuts import redirect
from django.urls import reverse
from datetime import date
from urllib.parse import urlencode

members = Profile.objects.best()[:5]
popular_tags = Tag.objects.popular()[:5]


def content_processor(request):
    return {
        'popular_tags': popular_tags,
        'members': members
    }


def get_paginator(request, obj_list, size):
    paginator = Paginator(obj_list, size)
    page = request.GET.get('page')
    return paginator.get_page(page)


def index(request):
    questions_list = Question.objects.new()
    questions = get_paginator(request, questions_list, 10)
    return render(request, 'index.html', {'object_list': questions})


def hot_questions(request):
    hot_questions_list = Question.objects.popular()
    hot_questions = get_paginator(request, hot_questions_list, 10)
    return render(request, 'select_questions.html', {'object_list': hot_questions, 'type': 'hot'})


def one_question(request, pk):
    question = Question.objects.get(id=pk)
    answers_list = Answer.objects.all_ans(pk)
    answers = get_paginator(request, answers_list, 5)
    return render(request, 'question.html', {'object_list': answers, 'question': question})


def login(request):
    alert = ""
    if request.method == 'GET':
        form = LoginForm()
    else:
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = auth.authenticate(request, **form.cleaned_data)
            if user is not None:
                auth.login(request, user)
                next = request.POST.get('next')
                if not next:
                    next = 'main'
                return redirect(next)
            else:
                alert = "No user with matching username and password found"
    return render(request, 'login.html', {'alert': alert, 'form': form})


@login_required
def logout(request):
    auth.logout(request)
    return redirect(reverse('main'))


def signup(request):
    alert = ""
    if request.method == 'GET':
        form = RegisterForm()
    else:
        form = RegisterForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            if User.objects.filter(email=form.cleaned_data['email']):
                alert = "Email already registered."
            else:
                user = User.objects.create_user(form.cleaned_data['username'],
                                                form.cleaned_data['email'], form.cleaned_data['password1'])
                profile = Profile(avatar=form.cleaned_data['avatar'], user_id=user.id)
                profile.save()
                user = auth.authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password1'])
                auth.login(request, user)
                return redirect('main')
    return render(request, 'signup.html', {'alert': alert, 'form': form})


@login_required
def ask(request):
    if request.method == 'GET':
        form = QuestionForm()
    else:
        form = QuestionForm(data=request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user.profile
            question.date = date.today()
            question.save()

            for elem in form.cleaned_data['tags'].split(', '):
                tag = Tag.objects.filter(name=elem)
                if elem and not tag:
                    tag = Tag(name=elem)
                    tag.save()
                else:
                    tag = tag[0]
                question.tags.add(tag.id)
            question.save()
            return redirect(reverse('one_question', kwargs={'pk': question.id}))
    return render(request, 'ask.html', {'form': form })


@login_required
def settings(request):
    if request.method == 'GET':
        form = SettingsForm(initial={'username': request.user.username, 'email':  request.user.email,
                                     'avatar': request.user.profile.avatar})
    else:
        form = SettingsForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            user = request.user
            user.username = form.cleaned_data['username']
            user.email = form.cleaned_data['email']
            user.profile.avatar = form.cleaned_data['avatar']
            user.profile.save()
            user.save()
            form = SettingsForm(initial={'username': request.user.username, 'email': request.user.email,
                                         'avatar': request.user.profile.avatar})
    return render(request, 'settings.html', {'form': form})


def tagged_questions(request, str):
    tagged_questions_list = Question.objects.tagged(str)
    tagged_questions = get_paginator(request, tagged_questions_list, 10)
    return render(request, 'select_questions.html', {'object_list': tagged_questions, 'type': 'tagged'})


@login_required
def answer(request):
    id = request.POST.get('pk')
    answer = Answer.objects.create(author_id=request.user.profile.id, question_id=id,
                                   date=date.today(), text=request.POST.get('text'))
    answer.save()
    return redirect(reverse('one_question', kwargs={'pk': id}))


def get_option(str):
    if str == 'like':
        return 1
    elif str == 'dislike':
        return -1


@login_required
@require_POST
def qvote(request):
    data = request.POST
    inc = get_option(data['action'])
    rating = 0
    error = ""

    question = Question.objects.get(id=data['qid'])
    like = QuestionLike.objects.filter(question_id=data['qid'], author_id=request.user.id)
    if question and not like:
        rating = question.rating + inc
        question.rating = F('rating') + inc
        question.save()
        QuestionLike.objects.create(question_id=question.id, author_id=request.user.profile.id,
                                    like=str(inc))
    else:
        error = "Error"

    return JsonResponse({'rating': rating, 'error': error})


@login_required
@require_POST
def avote(request):
    data = request.POST
    inc = get_option(data['action'])
    error = ""

    answer = Answer.objects.get(id=data['aid'])
    if answer and not AnswerLike.objects.filter(answer_id=data['aid'], author_id=request.user.id):
        AnswerLike.objects.create(answer_id=data['aid'], author_id=request.user.profile.id,
                                    like=str(inc))
    else:
        error = "Error"
    return JsonResponse({'rating': inc, 'error': error})

@login_required
@require_POST
def check(request):
    data = request.POST
    error = ""
    answer = Answer.objects.get(id=data['aid'])
    value = True
    if answer and answer.question.author.id == request.user.profile.id:
        if answer.checked:
            answer.checked = False
            answer.save()
            value = False
        else:
            answer.checked = True
            answer.save()
    else:
        error = "Error"
    return JsonResponse({'value': value, 'error': error})