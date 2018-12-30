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

# Create your views here.
def preview(request):
    current_user = request.user
    total_words = DoubleSyllable.objects.count()
    
    # already acessed word list
    accessed_word_list = DoubleSyllableAccess.objects.filter(user_id__exact=current_user.id).values('doublesyllable_id').distinct()
    accessed_words = accessed_word_list.count()

    # fetch one unaccessed word 
    word = DoubleSyllable.objects.exclude(id__in=accessed_word_list).values('word')[0]
    # fetch work list by word
    word_list = DoubleSyllable.objects.filter(word__exact=word['word'])
    template = loader.get_template('DoubleSyllable/preview.html')
    context = {
        'word_list': word_list,
        'total_words': total_words,
        'accessed_words': accessed_words + 1,
    }
    # mark this word as accessed
    for word in word_list:
        DoubleSyllableAccess.objects.create(user_id=current_user.id,doublesyllable_id=word.id,access_date=timezone.now()) 
    # return response
    return HttpResponse(template.render(context, request))

def test(request, doublesyllable_id):
    doublesyllable = get_object_or_404(DoubleSyllable, pk=doublesyllable_id)
    return render(request, 'DoubleSyllable/test.html', {'doublesyllable': doublesyllable})

def result(request, doublesyllable_id):
    doublesyllable = get_object_or_404(DoubleSyllable, pk=doublesyllable_id)
    # record test result to db
    DoubleSyllableTest.objects.create(user_id=request.user.id,
                                      doublesyllable_id=doublesyllable_id,
                                      test_date=timezone.now(),
                                      test_result=request.POST.get("test_result", ""),
                                      test_answer=request.POST.get("test_answer", "")
                                      )
    return HttpResponse("test result is recorded")