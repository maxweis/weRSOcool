from django.urls import path
from django.conf import settings
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.index, name='users-index'),
    path('<str:username>/', views.profile, name='user-profile'),
    path('<str:username>/update', views.update, name='user-update'),
    path('<str:username>/delete', views.delete, name='user-delete'),
    path('signup/', views.SignUp, name='signup'),
    path('login/', auth_views.LoginView.as_view(), {'template_name': 'login.html'}, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), {'template_name': 'logged_out.html'}, name='logout'),
]
