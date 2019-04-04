from django.shortcuts import render
from rso_manage.models import Registrations
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
