from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic
from django.contrib import messages
from django.urls import reverse
from django.db import connection
from .forms import RSOCreationForm, EditRSOForm, TagCreationForm
from .models import RSO, Registrations, Tag, MajorDist
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
            new_rso_member = Registrations(member=Member.objects.get(username=request.user.username), rso=RSO.objects.get(name=name), admin=True)
            new_rso_member.save()
            return redirect('home')
    else:
        form = RSOCreationForm()

    return render(request, 'rso_registration.html', {'form' : form})

def update_rso(request, rso_name,):
    rso = get_object_or_404(RSO, name=rso_name)
    if request.method == 'POST':
        form = EditRSOForm(request.POST, request.FILES, instance=rso)
        if form.is_valid():
            form.save()
            return redirect('/rsos/')
    else:
        form = EditRSOForm(instance=rso)
        return render(request, 'update_rso.html', {'form' : form, 'rso' : rso_name})

def rso_list(request):
    all_rsos = RSO.objects.raw('SELECT * FROM "rso_manage_rso"')
    return render(request, 'rso_list.html', {'all_rsos' : all_rsos})

def rso_list_search(request):
    if 'search_text' in request.GET:
        search = request.GET['search_text'].strip()
        rso_list_query = ''
        if (search == ''):
            rso_list_query = 'SELECT * FROM "rso_manage_rso"'
        else:
            rso_list_query = '\
                SELECT * FROM "rso_manage_rso"\
                WHERE name LIKE "%{}%"'.format(search)

        all_rsos = RSO.objects.raw(rso_list_query)
        return render(request, 'rso_list.html', {'all_rsos' : all_rsos})

def rso_profile(request, rso_name):
    rso = get_object_or_404(RSO, name=rso_name)
    rso_id = RSO.objects.get(name=rso_name).id
    member_registrations = Registrations.objects.raw('SELECT * FROM "rso_manage_registrations" WHERE rso_id = {}'.format(rso_id))
    member_names = list(set([m.member.username for m in member_registrations]))

    admin_registrations = Registrations.objects.raw('SELECT * FROM "rso_manage_registrations" WHERE rso_id = {} AND admin = 1'.format(rso_id))
    admin_names = list(set([m.member.username for m in admin_registrations]))
    tags = Tag.objects.raw('SELECT * FROM "rso_manage_tag" WHERE rso_id = {}'.format(rso_id))
    closest = nearest(rso)

    email_query =   'SELECT email \
                    FROM rso_manage_registrations JOIN users_member ON member_id = username \
                    WHERE rso_id = {}'.format(rso_id)


    cursor = connection.cursor()
    cursor.execute(email_query)
    emails = [x[0] for x in cursor.fetchall()]
    mailing_list = ", ".join(emails)


    return render(request, 'rso_profile.html', {'rso' : rso, 'member_registrations' : member_registrations, 'member_names' : member_names,
                                                'admin_registrations' : admin_registrations, 'admin_names' : admin_names, 'tags' : tags, 'closest' : closest,
                                                'mailing_list' : mailing_list})

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
    admin_registrations = Registrations.objects.raw('SELECT * FROM "rso_manage_registrations" WHERE rso_id={} AND admin=1'.format(rso.id))
    admin_names = list(set([m.member.username for m in admin_registrations]))
    if request.user.username in admin_names or request.user.username == 'admin':
        if Registrations.objects.filter(member=member, rso=rso).exists():
            Registrations.objects.filter(member=member, rso=rso).update(admin=True)
    return redirect('/rsos/'+rso_name+'/profile')

def unregister(request, rso_name):
    member = Member.objects.get(username=request.user.username)
    rso = RSO.objects.get(name=rso_name)
    if Registrations.objects.filter(member=member, rso=rso, admin=False).exists():
        Registrations.objects.get(member=member, rso=rso, admin=False).delete()
    return redirect('/rsos/'+rso_name+'/profile')

def unregister_as_admin(request, rso_name, username):
    rso_id = RSO.objects.get(name=rso_name).id
    admin_registrations = Registrations.objects.raw('SELECT * FROM "rso_manage_registrations" WHERE rso_id={} AND admin=1'.format(rso_id))
    admin_names = list(set([m.member.username for m in admin_registrations]))
    if request.user.username in admin_names and username not in admin_names:
        member = Member.objects.get(username=username)
        rso = RSO.objects.get(name=rso_name)
        if Registrations.objects.filter(member=member, rso=rso, admin=False).exists():
            Registrations.objects.get(member=member, rso=rso, admin=False).delete()
        return redirect('/rsos/'+rso_name+'/profile')

def removeadmin(request, rso_name, username):
    member = Member.objects.get(username=username)
    rso = RSO.objects.get(name=rso_name)
    admin_registrations = Registrations.objects.raw('SELECT * FROM "rso_manage_registrations" WHERE rso_id = {} AND admin=1'.format(rso.id))
    if len(admin_registrations) > 1 and Registrations.objects.filter(member=member, rso=rso).exists():
        Registrations.objects.filter(member=member, rso=rso).update(admin=False)
    return redirect('/rsos/'+rso_name+'/profile')

def rso_delete(request, rso_name):
    rso_id = RSO.objects.get(name=rso_name).id
    admin_registrations = Registrations.objects.raw('SELECT * FROM "rso_manage_registrations" WHERE rso_id={} AND admin=1'.format(rso_id))
    admin_names = list(set([m.member.username for m in admin_registrations]))
    if request.user.is_authenticated and (request.user.username in admin_names or request.user.username == 'admin'):
        try:
            cursor = connection.cursor()
            query = 'DELETE FROM "events_event" WHERE rso_id = {}'.format(rso_id)
            cursor.execute(query)
            query = 'DELETE FROM "rso_manage_tag" WHERE rso_id = {}'.format(rso_id)
            cursor.execute(query)
            query = 'DELETE FROM "rso_manage_registrations" WHERE rso_id = "{}"'.format(rso_id)
            cursor.execute(query)
            query = 'DELETE FROM "rso_manage_rso" WHERE rso_manage_rso.name = "{}"'.format(rso_name)
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
    admin_registrations = Registrations.objects.raw('SELECT * FROM "rso_manage_registrations" WHERE rso_id={} AND admin=1'.format(rso_id))
    admin_names = list(set([m.member.username for m in admin_registrations]))
    if request.user.username not in admin_names and request.user.username != 'admin':
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
    rso_id = RSO.objects.get(name=rso_name).id
    majors_query = 'SELECT major, COUNT(*) \
                    FROM rso_manage_registrations JOIN users_member ON member_id = username \
                    WHERE rso_id = {} \
                    GROUP BY major'.format(rso_id)
    cursor = connection.cursor()
    cursor.execute(majors_query)
    majors_dist = cursor.fetchall()
    for major, count in majors_dist:
        pie_chart.add(major, count)

    return pie_chart.render_django_response()

def rso_year_distribution(request,rso_name):
    pie_chart = pygal.Pie(title="Academic Year Distribution")

    rso_id = RSO.objects.get(name=rso_name).id
    years = {}
    for reg in Registrations.objects.raw("Select * from rso_manage_registrations where rso_id = {}".format(rso_id)):
        years[reg.member.academic_year] = years.get(reg.member.academic_year, 0) + 1

    for major, count in years.items():
        pie_chart.add(major, count)

    return pie_chart.render_django_response()

def mailing_list(request, rso_name):
    rso_id = RSO.objects.get(name=rso_name).id
    email_query =   'SELECT email \
                    FROM rso_manage_registrations JOIN users_member ON member_id = username \
                    WHERE rso_id = {}'.format(rso_id)

    cursor = connection.cursor()
    cursor.execute(email_query)
    emails = [x[0] for x in cursor.fetchall()]

    return render(request, 'rso_mailing_list.html', {'mailing_list': emails})

def remove_tag(request, rso_name, tag_name):
    rso_id = RSO.objects.get(name=rso_name).id
    delete_tag_query = 'DELETE FROM "rso_manage_tag" \
                        WHERE rso_id = "{}" AND tag = "{}"'.format(rso_id, tag_name)

    cursor = connection.cursor()
    cursor.execute(delete_tag_query)
    cursor.fetchall()

    return redirect('/rsos/'+rso_name+'/profile')
