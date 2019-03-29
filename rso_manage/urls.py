from django.urls import path
from django.conf.urls import include
from . import views

urlpatterns = [
    path('', views.rso_list, name='rso_list'),
    path('rso_registration/', views.AddRSO, name='rso_registration'),
    path('<str:rso_name>/members', views.rso_members, name='rso_members'),
    path('<str:rso_name>/register', views.register, name='register_for_rso'),
    path('<str:rso_name>/profile', views.rso_profile, name='profile_for_rso'),
    path('<str:rso_name>/delete', views.rso_delete, name='delete_rso'),
]
