from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.urls import reverse
from django.db import connection
from .forms import MemberCreationForm, EditProfileForm
from .models import Member
from rso_manage.models import Registrations
import pygal

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
    return render(request, 'index.html', {'all_members' : all_members})

def profile(request, username):
    member = get_object_or_404(Member, username=username)
    user = Member.objects.get(username=username)
    involvements = Registrations.objects.filter(member=user)
    if (len(involvements) == 0):
        involvements = None

    return render(request, 'profile.html', {'member' : member, 'involvements' : involvements})

def update(request, username,):
    member = get_object_or_404(Member, username=username)
    if request.method == 'POST':
        form = EditProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('/users/' + member.username + "/profile")
    else:
        form = EditProfileForm(instance=request.user)
        return render(request, 'update_profile.html', {'form' : form, 'member' : member})

def delete(request, username):
    if request.user.is_authenticated and username == request.user.username:
        try:
            cursor = connection.cursor()
            cursor.execute('DELETE FROM "users_member" WHERE users_member.username = "{}"'.format(request.user.username))
            connection.commit()
            messages.success(request, 'User deleted')
        except:
            messages.error(request, 'User not found')
    else:
        messages.error(request, 'You must be logged in')
    return redirect('/users/')

def get_college_dist(request, username):
    pie_chart = pygal.Pie(title='College Association of ' + username + '\'s RSOs')
    user_rsos_college_dist_query = '\
        SELECT r2.college_association, COUNT(*) \
        FROM rso_manage_registrations AS r1 JOIN rso_manage_rso as r2 ON r1.rso_id = r2.id \
        WHERE r1.member_id = "{}"'.format(username)

    cursor = connection.cursor()
    cursor.execute(user_rsos_college_dist_query)
    college_dist = cursor.fetchall()

    for college, count in college_dist:
        pie_chart.add(college, count)

    return pie_chart.render_django_response()

def get_rso_event_dist(request, username):
    pie_chart = pygal.Pie(title='RSO Distribution of Meetings Attended')

    user_rso_meeting_query = '\
        SELECT ev.rso_id, COUNT(*)\
        FROM events_attending AS att JOIN events_event as ev ON att.event_id = ev.name\
        WHERE att.user_id = "{}"\
        GROUP BY ev.rso_id'.format(username)

    cursor = connection.cursor()
    cursor.execute(user_rso_meeting_query)
    rso_dist = cursor.fetchall()

    for rso_name, count in rso_dist:
        pie_chart.add(rso_name, count)

    return pie_chart.render_django_response()
