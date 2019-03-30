from django import forms
from django.forms import ModelForm
from .models import RSO
import datetime

class RSOCreationForm(ModelForm):
    name = forms.CharField(max_length=64)
    now = datetime.datetime.now()
    date_established = forms.DateField(initial=now.today, widget=forms.SelectDateWidget(years=range(1960, int(now.year) + 1)))

    college_association = forms.CharField(max_length=64)
    icon = forms.ImageField(required=False)
    description = forms.CharField(widget=forms.Textarea(attrs={'rows': 3, 'cols':40}), max_length=1024)

    class Meta(ModelForm):
        model = RSO
        fields = ('name', 'date_established', 'college_association', 'icon', 'description')
        exclude = ['creator']
