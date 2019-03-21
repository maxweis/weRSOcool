from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class SignUpForm(UserCreationForm):
    user = UserCreationForm()
    icon = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ('username', 'icon', 'password1', 'password2')
