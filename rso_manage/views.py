from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic
from django.contrib import messages
from django.urls import reverse
from django.db import connection
from .forms import RSOCreationForm, TagCreationForm
from .models import RSO, Registrations, RSOAdmin, Tag, MajorDist
from users.models import Member
from .find_similar import nearest
import pygal

def AddRSO(request):
    if request.method == 'POST':
        form = RSOCreationForm(request.POST, request.FILES)
        if form.is_valid() and not RSO.objects.filter(name=form.cleaned_data.get('name')).exists():
            name = form.cleaned_data.get('name')
            date_established = form.cleaned_data.get('date_established')
            college_association = form.cleaned_data.get('college_association')
            icon = form.cleaned_data.get('icon')
            description = form.cleaned_data.get('description')
            form_save = form.save(commit=False)
            form.save()
            new_rso_member = Registrations(member=Member.objects.get(username=request.user.username), rso=RSO.objects.get(name=name))
            new_rso_member.save()
            new_rso_admin = RSOAdmin(member=Member.objects.get(username=request.user.username), rso=RSO.objects.get(name=name))
            new_rso_admin.save()
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
    member_names = list(set([m.member.username for m in member_registrations]))
    admin_registrations = RSOAdmin.objects.raw('SELECT * FROM "rso_manage_rsoadmin" WHERE rso_id = {}'.format(rso_id))
    admin_names = list(set([m.member.username for m in admin_registrations]))
    tags = Tag.objects.raw('SELECT * FROM "rso_manage_tag" WHERE rso_id = {}'.format(rso_id))
    closest = nearest(rso)


    return render(request, 'rso_profile.html', {'rso' : rso, 'member_registrations' : member_registrations, 'member_names' : member_names,
                                                'admin_registrations' : admin_registrations, 'admin_names' : admin_names, 'tags' : tags, 'closest' : closest,
                                                })

def register(request, rso_name):
    username = request.user.username
    member = Member.objects.get(username=username)
    rso = RSO.objects.get(name=rso_name)
    if not Registrations.objects.filter(member=member, rso=rso).exists():
        reg = Registrations(member=member, rso=rso)
        reg.save()
    return redirect('/rsos/'+rso_name+'/profile')

def makeadmin(request, rso_name, username):
    member = Member.objects.get(username=username)
    rso = RSO.objects.get(name=rso_name)
    admin_registrations = RSOAdmin.objects.raw('SELECT * FROM "rso_manage_rsoadmin" WHERE rso_id = {}'.format(rso.id))
    admin_names = list(set([m.member.username for m in admin_registrations]))
    if request.user.username in admin_names:
        if not RSOAdmin.objects.filter(member=member, rso=rso).exists():
            reg = RSOAdmin(member=member, rso=rso)
            reg.save()
    return redirect('/rsos/'+rso_name+'/profile')



def unregister(request, rso_name):
    member = Member.objects.get(username=request.user.username)
    rso = RSO.objects.get(name=rso_name)

    if Registrations.objects.filter(member=member, rso=rso).exists():
        Registrations.objects.get(member=member, rso=rso).delete()
    return redirect('/rsos/'+rso_name+'/profile')

def removeadmin(request, rso_name, username):
    member = Member.objects.get(username=username)
    rso = RSO.objects.get(name=rso_name)
    admin_registrations = RSOAdmin.objects.raw('SELECT * FROM "rso_manage_rsoadmin" WHERE rso_id = {}'.format(rso.id))
    if len(admin_registrations) > 1 and RSOAdmin.objects.filter(member=member, rso=rso).exists():
        RSOAdmin.objects.get(member=member, rso=rso).delete()
    return redirect('/rsos/'+rso_name+'/profile')

def rso_delete(request, rso_name):
    rso_id = RSO.objects.get(name=rso_name).id
    admin_registrations = RSOAdmin.objects.raw('SELECT * FROM "rso_manage_rsoadmin" WHERE rso_id = {}'.format(rso_id))
    admin_names = list(set([m.member.username for m in admin_registrations]))
    if request.user.is_authenticated and request.user.username in admin_names:
        try:
            cursor = connection.cursor()
            query = 'DELETE FROM "events_event" WHERE rso_id = {}'.format(rso_id)
            cursor.execute(query)
            query = 'DELETE FROM "rso_manage_rso" WHERE rso_manage_rso.name = "{}"'.format(rso_name)
            cursor.execute(query)
            query = 'DELETE FROM "rso_manage_rsoadmin" WHERE rso_manage_rsoadmin.name = "{}"'.format(rso_name)
            cursor.execute(query)
            query = 'DELETE FROM "rso_manage_registrations" WHERE rso_manage_registrations.name = "{}"'.format(rso_name)
            cursor.execute(query)
            connection.commit()
            messages.success(request, "RSO deleted")
        except Exception as E:
            print(E)
            messages.error(request, "RSO not found or you must be an admin of the RSO")
    else:
        messages.error(request, "You must be logged in to delete an RSO.")
    return redirect('/rsos/')

def add_tag(request, rso_name):
    event_rso = RSO.objects.get(name=rso_name)
    rso_id = RSO.objects.get(name=rso_name).id
    admin_registrations = RSOAdmin.objects.raw('SELECT * FROM "rso_manage_rsoadmin" WHERE rso_id = {}'.format(rso_id))
    admin_names = list(set([m.member.username for m in admin_registrations]))
    if request.user.username not in admin_names:
        return redirect('home')

    if request.method == 'POST':
        form = TagCreationForm(request.POST)
        if (form.is_valid()):
            form_save = form.save(commit=False)
            form_save.rso = event_rso
            form.save()
            return redirect('/rsos/' + rso_name + "/profile")
    else:
        form = TagCreationForm()

    return render(request, 'add_tag.html', {'form' : form})

def major_distribution(request, rso_name):

    pie_chart = pygal.Pie(title="Majors in Our RSO")

    majors_query = 'SELECT major, COUNT(*) \
                    FROM rso_manage_registrations JOIN users_member ON member_id = username \
                    GROUP BY major'


    cursor = connection.cursor()
    cursor.execute(majors_query)
    majors_dist = cursor.fetchall()

    for major, count in majors_dist:
        pie_chart.add(major, count)

    return pie_chart.render_django_response()
def rso_year_distribution(request,rso_name):
    pie_chart = pygal.Pie(title="Age Distribution")

    rso_id = RSO.objects.get(name=rso_name).id
    years = {}
    for reg in Registrations.objects.raw("Select * from rso_manage_registrations where rso_id = {}".format(rso_id)):
        years[reg.member.academic_year] = years.get(reg.member.academic_year, 0) + 1

    for major, count in years.items():
        pie_chart.add(major, count)

    return pie_chart.render_django_response()

