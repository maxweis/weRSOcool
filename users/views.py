from django.shortcuts import render
from django.views import generic
from django.contrib.auth import login, authenticate
from django.shortcuts import redirect
from .forms import MemberCreationForm
from .models import Member

def SignUp(request):
    if request.method == 'POST':
        form = MemberCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = MemberCreationForm()
    return render(request, 'signup.html', {'form' : form})

# class SignUp(generic.CreateView):
    # model = Member
    # form_class = MemberCreationForm
    # template_name = 'signup.html'
    # success_url = redirect('home')
    # # login(user)
