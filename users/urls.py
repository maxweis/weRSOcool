from django.conf.urls import url
from . import views
from django.urls import path

urlpatterns = [
    url(r'^$', views.index, name='users-index'),
    path("<rso_name>/", views.register, name='registrations'),
    url(r'^(?P<username>\w+)/$', views.profile, name='user-profile'),
    url(r'^(?P<username>\w+)/update$', views.update, name='user-update'),
    url(r'^(?P<username>\w+)/delete$', views.delete, name='user-delete'),
]
