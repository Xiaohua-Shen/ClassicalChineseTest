# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import get_object_or_404, render
from .models import DoubleSyllable
from .models import DoubleSyllableAccess
from .models import DoubleSyllableTestChoice
from .models import DoubleSyllableTest
from django.http import HttpResponse
from django.template import loader
from django.utils import timezone
from django.conf import settings
from django.shortcuts import redirect

# Create your views here.
def preview(request):
    if not request.user.is_authenticated:
        return redirect('/admin/login?next=%s' % (request.path))

    current_user = request.user
    total_words = DoubleSyllable.objects.count()
    
    # already acessed word list
    accessed_word_list = DoubleSyllableAccess.objects.filter(user_id__exact=current_user.id).values('doublesyllable_id').distinct()
    accessed_words = accessed_word_list.count()

    # fetch one unaccessed word 
    if total_words != accessed_words:
        word = DoubleSyllable.objects.exclude(id__in=accessed_word_list).values('word')[0]
        # fetch work list by word
        word_list = DoubleSyllable.objects.filter(word__exact=word['word'])
    else:
        word_list = None
    
    template = loader.get_template('DoubleSyllable/preview.html')
    context = {
        'word_list': word_list,
        'total_words': total_words,
        'accessed_words': accessed_words,
        'title': '预习'
    }
    # return response
    return HttpResponse(template.render(context, request))

def review(request):
    if not request.user.is_authenticated:
        return redirect('/admin/login?next=%s' % (request.path))

    current_user = request.user
    accessed_words_list = DoubleSyllableAccess.objects.filter(user_id__exact=current_user.id).values('doublesyllable_id').distinct()
    accessed_words = accessed_words_list.count()
    
    # already passed word list
    passed_word_list = DoubleSyllableTest.objects.filter(user_id__exact=current_user.id,test_result=1).values('doublesyllable_id').distinct()
    passed_words = passed_word_list.count()

    # get unpassed word list
    unpassed_word_list = accessed_words_list.difference(passed_word_list)

    # fetch one unpassed word 
    if accessed_words != passed_words:
        word = DoubleSyllable.objects.filter(id__in=unpassed_word_list).values('word')[0]
        # fetch work list by word
        word_list = DoubleSyllable.objects.filter(word__exact=word['word'])
    else:
        word_list = None

    template = loader.get_template('DoubleSyllable/preview.html')
    context = {
        'word_list': word_list,
        'total_words': accessed_words,
        'accessed_words': passed_words,
        'title': '复习'
    }
    # return response
    return HttpResponse(template.render(context, request))

def index(request):
    if not request.user.is_authenticated:
        return redirect('/admin/login?next=%s' % (request.path))
    
    current_user = request.user
    # total word
    total_words = DoubleSyllable.objects.count()
    
    # already acessed word count
    accessed_words = DoubleSyllableAccess.objects.filter(user_id__exact=current_user.id).values('doublesyllable_id').distinct().count()

    # pass test word count
    passed_words = DoubleSyllableTest.objects.filter(user_id__exact=current_user.id,test_result=1).values('doublesyllable_id').distinct().count()

    # prepare return page
    template = loader.get_template('DoubleSyllable/index.html')
    context = {
        'total_words': total_words,
        'accessed_words': accessed_words,
        'passed_words': passed_words,
        'user': current_user.username
    }
    # return page
    return HttpResponse(template.render(context, request))

def result(request, doublesyllable_id):
    doublesyllable = get_object_or_404(DoubleSyllable, pk=doublesyllable_id)
    # record test result to db
    DoubleSyllableTest.objects.create(user_id=request.user.id,
                                      doublesyllable_id=doublesyllable_id,
                                      test_date=timezone.now(),
                                      test_result=request.POST.get("test_result", ""),
                                      test_answer=request.POST.get("test_answer", "")
                                      )
    # record access log to db
    DoubleSyllableAccess.objects.create(user_id=request.user.id,
                                        doublesyllable_id=doublesyllable_id,
                                        access_date=timezone.now()
                                        )
    # return page 
    return HttpResponse("test result is recorded")