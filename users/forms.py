from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Member

class MemberCreationForm(UserCreationForm):
    ACAD_YEAR_CHOICES = (
            ('FR', 'Freshman'),
            ('SO', 'Sophomore'),
            ('JR', 'Junior'),
            ('SR', 'Senior'),
            ('GR', 'Graduate')
    )

    user = UserCreationForm()
    major = forms.CharField(max_length=64)
    academic_year = forms.ChoiceField(choices=ACAD_YEAR_CHOICES)
    resume = forms.FileField(required=False)
    icon = forms.ImageField(required=False)

    class Meta(UserCreationForm):
        model = Member
        fields = ('username', 'first_name', 'last_name', 'major', 'academic_year', 'email' ,'icon', 'password1', 'password2')
