# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import get_object_or_404, render
from .models import SWord
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

    # get word list
    word_list = SWord.objects.all().values('sword').distinct()

    # prepare return page
    template = loader.get_template('s_word/index.html')
    context = {
        'word_list': word_list,
        'user': current_user.username
    }
    # return page
    return HttpResponse(template.render(context, request))
