from django.urls import path
from django.conf.urls import include
from . import views

urlpatterns = [
    path('rso_colleges_chart', views.rso_colleges_chart, name='rso_colleges_chart'),
    path('', views.analytics_home, name='analytics_home'),
    path('rso_users_pie_chart', views.rso_users_pie_chart, name='rso_users_pie_chart'),
]
