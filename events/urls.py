from django.urls import path
from django.conf.urls import include
from . import views

urlpatterns = [
    path('events/', views.list_all_events, name='event_home'),
    path('rsos/<rso_name>/add_event', views.AddEvent, name='add_event'),
    path('rsos/<rso_name>/events', views.display_events, name='list_events'),
    path('rsos/<rso_name>/<event>/attend', views.attend_event, name='attend_event'),
]
