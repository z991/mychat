from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<room_name>[^/]+)/$', views.room, name='room'),
    url(r'^test/$', views.test, name='test'),
    url(r'^test_message/ok/$', views.test_send, name='test_send'),

]