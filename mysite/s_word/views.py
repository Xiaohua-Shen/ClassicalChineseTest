# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import get_object_or_404, render
from .models import SWord,SWordTest,SWordTest1Choice,SWordUserQuestionByWord,SWordQuestionByWord
from django.http import HttpResponse
from django.template import loader
from django.utils import timezone
from django.conf import settings
from django.shortcuts import redirect

# Create your views here.

def index(request):
    if not request.user.is_authenticated:
        return redirect('/admin/login?next=%s' % (request.path))
    
    current_user = request.user

    # get inprogress or passed word list
    start_word_list = SWordUserQuestionByWord.objects.filter(user_id=current_user.id)

    # get not start word list
    notstart_word_list = SWordQuestionByWord.objects.values('sword').difference(start_word_list.values('sword'))

    # prepare return page
    template = loader.get_template('s_word/index.html')
    context = {
        'start_word_list': start_word_list,
        'notstart_word_list': notstart_word_list,
        'user': current_user.username
    }
    # return page
    return HttpResponse(template.render(context, request))

def word(request):
    if not request.user.is_authenticated:
        return redirect('/admin/login?next=%s' % (request.path))
    
    sword = request.GET.get('sword', '')
    sword_list = SWord.objects.filter(sword=sword)
    pinyin_list = sword_list.exclude(pinyin="").values('pinyin').distinct()
    word_class_list = sword_list.values('word_class').distinct()
    meaning_list = sword_list.values('meaning').distinct()

    pinyin_questions = SWordTest1Choice.objects.filter(sword_id__in=sword_list, test_type='拼音').values('sword_id').distinct().count()
    word_class_questions = SWordTest1Choice.objects.filter(sword_id__in=sword_list, test_type='词性').values('sword_id').distinct().count()
    meaning_questions = SWordTest1Choice.objects.filter(sword_id__in=sword_list, test_type='含义').values('sword_id').distinct().count()

    pinyin_passed = SWordTest.objects.filter(sword_id__in=sword_list, test_type='拼音', user_id=request.user.id, test_result=1).values('sword_id').distinct().count()
    word_class_passed = SWordTest.objects.filter(sword_id__in=sword_list, test_type='词性', user_id=request.user.id, test_result=1).values('sword_id').distinct().count()
    meaning_passed = SWordTest.objects.filter(sword_id__in=sword_list, test_type='含义', user_id=request.user.id, test_result=1).values('sword_id').distinct().count()

    if pinyin_questions == 0:
        pinyin_test_status = "notest"
    elif pinyin_questions == pinyin_passed:
        pinyin_test_status = "passed"
    elif pinyin_passed == 0:
        pinyin_test_status = "notstart"
    elif pinyin_test_status = "inprogress"

    if word_class_questions == 0:
        word_class_test_status = "notest"
    elif word_class_questions == word_class_passed:
        word_class_test_status = "passed"
    elif word_class_passed == 0:
        word_class_test_status = "notstart"
    elif word_class_test_status = "inprogress"

    if meaning_questions == 0:
        meaning_test_status = "notest"
    elif meaning_questions == meaning_passed:
        meaning_test_status = "passed"
    elif meaning_passed == 0:
        meaning_test_status = "notstart"
    elif meaning_test_status = "inprogress"

    # prepare return page
    template = loader.get_template('s_word/word.html')
    context = {
        'sword': sword,
        'pinyin_list': pinyin_list,
        'word_class_list': word_class_list,
        'meaning_list': meaning_list,
        'user': request.user.username,
        'pinyin_test_status': pinyin_test_status,
        'word_class_test_status': word_class_test_status,
        'meaning_test_status': meaning_test_status
    }
    # return page
    return HttpResponse(template.render(context, request))

def test(request):
    if not request.user.is_authenticated:
        return redirect('/admin/login?next=%s' % (request.path))
    
    sword = request.GET.get('sword', '')
    test_type = request.GET.get('test_type', '')
    word_list = SWord.objects.filter(sword=sword)

    # prepare return page
    template = loader.get_template('s_word/test.html')
    context = {
        'sword': sword,
        'word_list': word_list,
        'user': request.user.username,
        'test_type': test_type
    }
    # return page
    return HttpResponse(template.render(context, request))

def result(request, word_id):
    sword = get_object_or_404(SWord, pk=word_id)
    # record test result to db
    SWordTest.objects.create(user_id=request.user.id,
                                      sword_id=word_id,
                                      test_date=timezone.now(),
                                      test_type=request.POST.get("test_type", ""),
                                      test_result=request.POST.get("test_result", ""),
                                      test_answer=request.POST.get("test_answer", "")
                                      )
    # return page 
    return HttpResponse("test result is recorded")