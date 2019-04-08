from django.shortcuts import render
from rso_manage.models import Registrations, RSO
from users.models import Member
from django.db import connection
import pygal
from django.db import connection

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

    get_college_assoc_query = 'SELECT r2.college_association, COUNT(*) \
                                FROM rso_manage_registrations AS r1 JOIN rso_manage_rso as r2 ON r1.rso_id = r2.id \
                                GROUP BY r2.college_association'

    cursor = connection.cursor()
    cursor.execute(get_college_assoc_query)
    college_assoc = cursor.fetchall()  

    for college, count in college_assoc:
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

def majors(request):
    pie_chart = pygal.Pie(title="Majors")


    majors_query = 'SELECT major, COUNT(*) \
                    FROM rso_manage_registrations JOIN users_member ON member_id = username \
                    GROUP BY major'


    cursor = connection.cursor()
    cursor.execute(majors_query)
    majors_dist = cursor.fetchall()
    for major, count in majors_dist:
        pie_chart.add(major, count)

    return pie_chart.render_django_response()
