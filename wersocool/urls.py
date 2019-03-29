from django.conf.urls import include
from django.urls import path
from django.contrib import admin
from django.views.generic.base import TemplateView
from django.conf import settings
from django.conf.urls.static import static
from users import urls as users_urls
from rso_manage import urls as rso_urls

urlpatterns = [
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('admin/', admin.site.urls),
    path('users/', include(users_urls)),
    path('rsos/', include(rso_urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
