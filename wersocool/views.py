from django.shortcuts import render, redirect, get_object_or_404
from django.db import connection
from rso_manage.models import RSO


def home_view(request):
    featured_rsos_query = 'SELECT * FROM "rso_manage_rso" ORDER BY RANDOM() LIMIT 3;'
    featured_rsos = RSO.objects.raw(featured_rsos_query)

    return render(request, 'home.html', {'featured_rsos' : featured_rsos})

def github_redirect(request):
    return redirect('https://github.com/maxweis/weRSOcool')

def youtube_video_redirect(request):
    return redirect("https://www.youtube.com/watch?v=ZvQU5mgabag")
