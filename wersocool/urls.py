from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.views.generic.base import TemplateView
from users import views as users_views
from users import urls as users_urls
from rso_manage import views as rso_views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name='home.html'), name='home'),
    url(r'^login/$', auth_views.LoginView.as_view(), {'template_name': 'login.html'}, name='login'),
    url(r'^logout/$', auth_views.LogoutView.as_view(), {'template_name': 'logged_out.html'}, name='logout'),
    url(r'^admin/', admin.site.urls),
    url(r'^signup/$', users_views.SignUp, name='signup'),
    url(r'^users/', include(users_urls)),
    url(r'^rso_registration', rso_views.AddRSO, name='rso_registration'),
    path("rso/", users_views.rso_list, name='rso_list'),
    path("<rso_name>/register", users_views.register, name='registrations'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
