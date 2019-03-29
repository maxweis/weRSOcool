from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.urls import reverse
from django.db import connection
from .forms import MemberCreationForm, EditProfileForm
from .models import Member, Registrations
from rso_manage.models import RSO

def SignUp(request):
    if request.method == 'POST':
        form = MemberCreationForm(request.POST, request.FILES)
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
    all_members = Member.objects.raw('SELECT username FROM "users_member" WHERE username <> "admin"')
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
        return render(request, 'users/update_profile.html', {'form' : form, 'member' : member})

def delete(request, username):
    if request.user.is_authenticated and username == request.user.username:
        try:
            cursor = connection.cursor()
            cursor.execute('DELETE FROM "users_member" WHERE users_member.username = "{}"'.format(request.user.username))
            connection.commit()
            messages.success(request, "User deleted")
        except:
            messages.error(request, "User not found")
    else:
        messages.error(request, "You must be logged in")
    return redirect('/users/')


def rso_list(request):
    all_rsos = RSO.objects.raw('SELECT * FROM "rso_manage_rso"')
    return render(request, 'users/rso_list.html', {'all_rsos' : all_rsos})

def rso_profile(request, rso_name):
    rso = get_object_or_404(RSO, name=rso_name)
    return render(request, 'users/rso_profile.html', {'rso' : rso})

def register(request, rso_name):
    username = request.user.username
    member = Member.objects.get(username=username)
    rso = RSO.objects.get(name=rso_name)

    reg = Registrations(member=member, rso=rso)
    reg.save()
    return render(request, 'users/register_success.html', {'name' : username, 'rso' : rso_name})

def rso_members(request, rso_name):
    rso_id = RSO.objects.get(name=rso_name).id
    member_registrations = Registrations.objects.raw("SELECT * FROM users_registrations WHERE rso_id = {}".format(rso_id))
    return render(request, 'users/rso_members.html', {"member_registrations" : member_registrations})

def rso_delete(request, rso_name):
    if request.user.is_authenticated:
        try:
            cursor = connection.cursor()
            query = 'DELETE FROM "rso_manage_rso" WHERE rso_manage_rso.name = "{}" AND rso_manage_rso.creator = "{}"'.format(rso_name, request.user.username)
            cursor.execute(query)
            connection.commit()
            messages.success(request, "RSO deleted")
        except:
            messages.error(request, "RSO not found or you must be the creator of the RSO")
    else:
        messages.error(request, "You must be logged in to delete an RSO.")
    return redirect('/rso/')
