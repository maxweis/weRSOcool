from django import forms
from django.forms import ModelForm
from .models import Event

class EventCreationForm(ModelForm):
    name = forms.CharField(max_length=64)
    time_begin = forms.DateTimeField(widget=forms.SelectDateWidget())
    time_end = forms.DateTimeField(widget=forms.SelectDateWidget())
    place = forms.CharField(max_length=64)

    class Meta(ModelForm):
        model = Event
        fields = ('name', 'time_begin', 'time_end',  'place')
        exclude = ['rso']