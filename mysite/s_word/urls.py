from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<sword>)/preview/$', views.preview, name='preview'),
]
