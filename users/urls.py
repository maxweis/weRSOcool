from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='users-index'),
    path('rso_users_pie_chart', views.rso_users_pie_chart, name='rso_users_pie_chart'),
    path('<username>/profile', views.profile, name='user-profile'),
    path('<username>/update', views.update, name='user-update'),
    path('<username>/delete', views.delete, name='user-delete'),
]
