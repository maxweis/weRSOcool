from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .forms import MemberCreationForm
from .models import Member

class MemberAdmin(UserAdmin):
    add_form = MemberCreationForm
    model = Member
    list_display = ['email', 'username']

admin.site.register(Member, MemberAdmin)
