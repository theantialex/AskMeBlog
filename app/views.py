from django.shortcuts import render
from django.core.paginator import Paginator
from django.template import RequestContext
from .models import *

members = Profile.objects.all()[:5]
popular_tags = Tag.objects.values('name').distinct()[:5]
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
    context = RequestContext(request, content_processor(request))
    context.push({'object_list': questions})
    return render(request, 'index.html', context.flatten())


def hot_questions(request):
    hot_questions_list = Question.objects.popular()
    hot_questions = get_paginator(request, hot_questions_list, 10)
    context = RequestContext(request, content_processor(request))
    context.push({'object_list': hot_questions})
    context.push({'type': 'hot'})
    return render(request, 'select_questions.html', context.flatten())


def one_question(request, pk):
    question = Question.objects.get(id=pk)
    answers_list = Answer.objects.all_ans(pk)
    answers = get_paginator(request, answers_list, 5)
    context = RequestContext(request, content_processor(request))
    context.push({'object_list': answers})
    context.push({'question': question})
    return render(request, 'question.html', context.flatten())


def login(request):
    context = RequestContext(request, content_processor(request))
    context.push({'alert': alert})
    return render(request, 'login.html', context.flatten())


def signup(request):
    context = RequestContext(request, content_processor(request))
    context.push({'alert': alert})
    return render(request, 'signup.html', context.flatten())


def ask(request):
    context = RequestContext(request, content_processor(request))
    return render(request, 'ask.html', context.flatten())


def settings(request):
    context = RequestContext(request, content_processor(request))
    return render(request, 'settings.html', context.flatten())


def tagged_questions(request, str):
    tagged_questions_list = Question.objects.tagged(str)
    tagged_questions = get_paginator(request, tagged_questions_list, 10)
    context = RequestContext(request, content_processor(request))
    context.push({'object_list': tagged_questions})
    context.push({'type': 'tagged'})
    return render(request, 'select_questions.html', context.flatten())