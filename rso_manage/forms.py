from django import forms
from django.forms import ModelForm
from bootstrap_datepicker_plus import DatePickerInput
from .models import RSO

class RSOCreationForm(ModelForm):
    name = forms.CharField(max_length=64)
    date_established = forms.DateField(widget=DatePickerInput)

    college_association = forms.CharField(max_length=64)
    icon = forms.ImageField(required=False)
    description = forms.CharField(widget=forms.Textarea(attrs={'rows': 3, 'cols':40}), max_length=1024)

    class Meta(ModelForm):
        model = RSO
        fields = ('name', 'date_established', 'college_association', 'icon', 'description')
