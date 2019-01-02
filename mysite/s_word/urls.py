from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^word/$', views.word, name='word'),
    url(r'^test/$', views.test, name='test'),
    url(r'^errortest/$', views.errortest, name='errortest'),
    url(r'^randomtest/$', views.randomtest, name='randomtest'),
    url(r'^(?P<word_id>[0-9]+)/result/$', views.result, name='result'),
]
