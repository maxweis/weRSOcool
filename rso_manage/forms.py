from django import forms
from django.forms import ModelForm
from bootstrap_datepicker_plus import DatePickerInput
from .models import RSO, Tag

COLLEGES = [
        'None',
        'Agricultural, Consumer, and Environmental Sciences (ACES)',
        'Applied Health Sciences (AHS)',
        'Education (EDU)',
        'Engineering (ENG)',
        'Fine and Applied Arts (FAA)',
        'Liberal Arts and Sciences (LAS)',
        'Media (COM)',
        'Division of General Studies (DGS)',
        'Gies College of Business (BUS)',
        'School of Social Work (SSW)',
        ]

class RSOCreationForm(ModelForm):
    name = forms.CharField(max_length=64)
    date_established = forms.DateField(widget=DatePickerInput)

    college_association = forms.ChoiceField(choices=[(x, x) for x in COLLEGES])
    # college_association = forms.CharField(max_length=64)
    icon = forms.ImageField(required=False)
    description = forms.CharField(widget=forms.Textarea(attrs={'rows': 3, 'cols':40}), max_length=1024)

    class Meta(ModelForm):
        model = RSO
        fields = ('name', 'date_established', 'college_association', 'icon', 'description')

class EditRSOForm(ModelForm):
    date_established = forms.DateField(widget=DatePickerInput)
    college_association = forms.ChoiceField(choices=[(x, x) for x in COLLEGES])

    class Meta:
        model = RSO
        fields = ('name', 'date_established', 'college_association', 'description')

class TagCreationForm(ModelForm):

    class Meta(ModelForm):
        model = Tag
        fields = ('tag', )
        exclude = ['rso']
