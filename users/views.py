from django.shortcuts import render
from django.views import generic
from django.contrib.auth import login, authenticate
from django.shortcuts import redirect
from django.http import Http404
from .forms import MemberCreationForm
from .models import Member
from query import query

def SignUp(request):
    if request.method == 'POST':
        form = MemberCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            major = form.cleaned_data.get('major')
            resume = form.cleaned_data.get('resume')
            icon = form.cleaned_data.get('icon')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = MemberCreationForm()
    return render(request, 'signup.html', {'form' : form})

def index(request):
    all_members = Member.objects.raw('SELECT username FROM "users_member"') 
    return render(request, 'users/index.html', {'all_members' : all_members})

def profile(request, username):
    try:
        member = Member.objects.get(username=username)
    except Member.DoesNotExist:
        raise Http404("User does not exist.")
    return render(request, 'users/profile.html', {'member' : member})
