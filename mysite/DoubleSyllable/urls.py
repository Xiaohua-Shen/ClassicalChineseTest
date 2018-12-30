from django.conf.urls import url

from . import views

app_name = 'DoubleSyllable'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^preview/$', views.preview, name='preview'),
    url(r'^review/$', views.review, name='review'),
    url(r'^review2/$', views.review2, name='review2'),
    url(r'^(?P<doublesyllable_id>[0-9]+)/result/$', views.result, name='result'),
]
