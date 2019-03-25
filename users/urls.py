from django.conf.urls import url
from . import views
from django.urls import path

urlpatterns = [
    url(r'^$', views.index, name='users-index'),
    path("registrations/", views.registrations, name='registrations'),
    url(r'^(?P<username>\w+)/$', views.profile, name='user-profile'),
]
