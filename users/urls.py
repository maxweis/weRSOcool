from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='users-index'),
    path('<username>/profile', views.profile, name='user-profile'),
    path('<username>/update', views.update, name='user-update'),
    path('<username>/delete', views.delete, name='user-delete'),
    path('<username>/user_rso_college_dist', views.get_college_dist, name='user-rso-college-dist'),
    path('<username>/user_event_rso_dist', views.get_rso_event_dist, name='user-event-rso-dist')
]
