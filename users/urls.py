from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='users-index'),
    path('<username>/profile', views.profile, name='user-profile'),
    path('<username>/update', views.update, name='user-update'),
    path('<username>/delete', views.delete, name='user-delete'),
]
