from django.conf.urls import include
from django.urls import path
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.views.generic.base import TemplateView
from django.conf import settings
from django.conf.urls.static import static
from users import urls as users_urls
from users import views as users_views
from rso_manage import urls as rso_urls

urlpatterns = [
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('signup/', users_views.SignUp, name='signup'),
    path('login/', auth_views.LoginView.as_view(), {'template_name': 'login.html'}, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), {'template_name': 'logged_out.html'}, name='logout'),
    path('admin/', admin.site.urls),
    path('users/', include(users_urls)),
    path('rsos/', include(rso_urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
