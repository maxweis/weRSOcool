from django.contrib import admin

# Register your models here.
from .models import RSO, Registrations

admin.site.register(RSO)
admin.site.register(Registrations)
