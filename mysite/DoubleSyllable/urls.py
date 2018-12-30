from django.conf.urls import url

from . import views

app_name = 'DoubleSyllable'
urlpatterns = [
    url(r'^/$', views.index, name='index'),
    url(r'^preview/$', views.preview, name='preview'),
    url(r'^(?P<doublesyllable_id>[0-9]+)/result/$', views.result, name='result'),
]
