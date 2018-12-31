from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^word/$', views.word, name='word'),
    url(r'^test/$', views.test, name='test'),
    url(r'^(?P<word_id>[0-9]+)/result/$', views.result, name='result'),
]
