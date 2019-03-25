from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.contrib.auth import login, authenticate
from django.shortcuts import redirect
# from django.http import Http404
from .forms import MemberCreationForm
from .models import Member
from rso_manage.models import RSO

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
    member = get_object_or_404(Member, username=username)
    return render(request, 'users/profile.html', {'member' : member})

def registrations(request):
    #important change this this is just some random stuff i added
    return None

def rso_list(request):
    all_rsos = RSO.objects.raw('SELECT * FROM "rso_manage_rso"')
    return render(request, 'users/rso_list.html', {'all_rsos' : all_rsos})
