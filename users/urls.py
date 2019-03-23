from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='users-index'),
    url(r'^(?P<username>\w+)/$', views.profile, name='user-profile'),
]
