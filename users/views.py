from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.urls import reverse
from .forms import MemberCreationForm, EditProfileForm
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

def update(request, username,):
    member = get_object_or_404(Member, username=username)
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('/users/'+member.username) # I couldn't get this to be not ugly
    else:
        form = EditProfileForm(instance=request.user)
        return render(request, 'users/update_profile.html', {'form' : form, 'member':member})

def delete(request, username):
    if request.user.is_authenticated and username == request.user.username:
        try:
            Member.objects.filter(username = username).delete()
            messages.success(request, "User deleted")
        except:
            messages.error(request, "User not found")
    else:
        messages.error(request, "You must be logged in")
    return redirect('/users/')
    # return render(request, 'home.html')

    # to_delete = Member.objects.raw('DELETE FROM "users_member" WHERE users_member.username = username')
    # Member.save(request)
    # all_members = Member.objects.raw('SELECT * FROM "users_member"')
    # return render(request, 'users/index.html', {'all_members' : all_members})

def registrations(request):
    #important change this this is just some random stuff i added
    return None

def rso_list(request):
    all_rsos = RSO.objects.raw('SELECT * FROM "rso_manage_rso"')
    return render(request, 'users/rso_list.html', {'all_rsos' : all_rsos})
