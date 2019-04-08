from django.shortcuts import render
from rso_manage.models import Registrations, RSO
from users.models import Member
import pygal

def rso_users_pie_chart(request):
    pie_chart = pygal.Pie(title="Member RSO distribution")

    clubs = {}
    for reg in Registrations.objects.all():
        clubs[reg.rso.name] = clubs.get(reg.rso.name, 0) + 1

    for club, count in clubs.items():
        pie_chart.add(club, count)

    return pie_chart.render_django_response()

def analytics_home(request):
    return render(request, "analytics_home.html")

def rso_colleges_chart(request):
    pie_chart = pygal.Pie(title="Colleges Distribution")

    colleges = {}
    for rso in RSO.objects.raw("Select * from rso_manage_rso"):
        colleges[rso.college_association] = colleges.get(rso.college_association, 0) + 1

    for college, count in colleges.items():
        pie_chart.add(college, count)

    return pie_chart.render_django_response()

def users_years(request):
    pie_chart = pygal.Pie(title="Years")

    clubs = {}
    for mem in Member.objects.raw("Select * from users_member"):
        if mem.username != "admin":
            clubs[mem.academic_year] = clubs.get(mem.academic_year, 0) + 1

    for club, count in clubs.items():
        pie_chart.add(club, count)

    return pie_chart.render_django_response()
