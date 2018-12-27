from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^preview/$', views.preview, name='preview'),
]
