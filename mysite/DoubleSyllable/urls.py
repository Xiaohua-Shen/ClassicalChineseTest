from django.conf.urls import url

from . import views

app_name = 'DoubleSyllable'
urlpatterns = [
    url(r'^preview/$', views.preview, name='preview'),
    url(r'^(?P<doublesyllable_id>[0-9]+)/test/$', views.test, name='test'),
    url(r'^(?P<doublesyllable_id>[0-9]+)/result/$', views.test, name='result'),
]
