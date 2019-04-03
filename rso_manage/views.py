from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic
from django.contrib import messages
from django.urls import reverse
from django.db import connection
from .forms import RSOCreationForm
from .models import RSO
from .models import Registrations
from users.models import Member

def AddRSO(request):
    if request.method == 'POST':
        form = RSOCreationForm(request.POST, request.FILES)
        if form.is_valid():
            name = form.cleaned_data.get('name')
            date_established = form.cleaned_data.get('date_established')
            college_association = form.cleaned_data.get('college_association')
            icon = form.cleaned_data.get('icon')
            description = form.cleaned_data.get('description')
            form_save = form.save(commit=False)
            form_save.creator = request.user.username
            form.save()
            return redirect('home')
    else:
        form = RSOCreationForm()

    return render(request, 'rso_registration.html', {'form' : form})

def rso_list(request):
    all_rsos = RSO.objects.raw('SELECT * FROM "rso_manage_rso"')
    return render(request, 'rso_list.html', {'all_rsos' : all_rsos})

def rso_profile(request, rso_name):
    rso = get_object_or_404(RSO, name=rso_name)
    rso_id = RSO.objects.get(name=rso_name).id
    member_registrations = Registrations.objects.raw('SELECT * FROM "rso_manage_registrations" WHERE rso_id = {}'.format(rso_id))
    member_names = [m.member.username for m in member_registrations]
    member_names = list(set(member_names))
    # print("names "+str(member_names))
    return render(request, 'rso_profile.html', {'rso' : rso, 'member_registrations' : member_registrations, 'member_names' : member_names})

def register(request, rso_name):
    username = request.user.username
    member = Member.objects.get(username=username)
    rso = RSO.objects.get(name=rso_name)
    if not Registrations.objects.filter(member=member, rso=rso).exists():
        reg = Registrations(member=member, rso=rso)
        reg.save()
    return redirect('/rsos/'+rso_name+'/profile')

def unregister(request, rso_name):
    username = request.user.username
    member = Member.objects.get(username=username)
    rso = RSO.objects.get(name=rso_name)
    if Registrations.objects.filter(member=member, rso=rso).exists():
        Registrations.objects.get(member=member, rso=rso).delete()
    return redirect('/rsos/'+rso_name+'/profile')
    return render(request, 'rso_list.html', {'all_rsos' : all_rsos})

def rso_delete(request, rso_name):
    rso_id = RSO.objects.get(name=rso_name).id
    if request.user.is_authenticated:
        try:
            cursor = connection.cursor()
            query = 'DELETE FROM "events_event" WHERE rso_id = {}'.format(rso_id)
            cursor.execute(query)
            query = 'DELETE FROM "rso_manage_rso" WHERE rso_manage_rso.name = "{}" AND rso_manage_rso.creator = "{}"'.format(rso_name, request.user.username)
            cursor.execute(query)
            connection.commit()
            messages.success(request, "RSO deleted")
        except Exception as E:
            print(E)
            messages.error(request, "RSO not found or you must be the creator of the RSO")
    else:
        messages.error(request, "You must be logged in to delete an RSO.")
    return redirect('/rsos/')
