from django.shortcuts import render
from django.shortcuts import redirect
from .forms import RSOCreationForm

def AddRSO(request):
    date_established = "DEFAULT"
    if request.method == 'POST':
        form = RSOCreationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            name = form.cleaned_data.get('name')
            date_established = form.cleaned_data.get('date_established')
            college_association = form.cleaned_data.get('college_association')
            icon = form.cleaned_data.get('icon')
            creator = request.user
            return redirect('home')
    else:
        form = RSOCreationForm()

    return render(request, 'rso_registration.html', {'form' : form})
