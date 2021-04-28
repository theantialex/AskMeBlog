from django.shortcuts import render
from django.core.paginator import Paginator
from django.template import RequestContext
from .models import *

members = Profile.objects.best()[:5]
popular_tags = Tag.objects.popular()[:5]
alert = ""
user = Profile.objects.all()[0]


def content_processor(request):
    return {
        'popular_tags': popular_tags,
        'members': members,
        'user': user
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
    context = RequestContext(request, content_processor(request))
    return render(request, 'login.html', {'alert': alert})


def signup(request):
    return render(request, 'signup.html', {'alert': alert})


def ask(request):
    return render(request, 'ask.html', {})


def settings(request):
    return render(request, 'settings.html', {})


def tagged_questions(request, str):
    tagged_questions_list = Question.objects.tagged(str)
    tagged_questions = get_paginator(request, tagged_questions_list, 10)
    return render(request, 'select_questions.html', {'object_list': tagged_questions, 'type': 'tagged'})