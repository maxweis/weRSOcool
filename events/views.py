from django.shortcuts import render, redirect, get_object_or_404
from .forms import EventCreationForm
from rso_manage.models import RSO

def AddEvent(request, rso_name):
    event_rso = RSO.objects.get(name=rso_name)
    if request.user.username != event_rso.creator:
        return redirect('home')

    if request.method == 'POST':
        form = EventCreationForm(request.POST)
        if (form.is_valid()):
            name = form.cleaned_data.get('name')
            time_begin = form.cleaned_data.get('time_begin')
            time_end = form.cleaned_data.get('time_end')
            place = form.cleaned_data.get('place')
            form_save = form.save(commit=False)
            form_save.rso = event_rso
            form.save()
            return redirect('home')
    else:
        form = EventCreationForm()

    return render(request, 'add_event.html', {'form' : form})

def display_events(request, rso_name):
    rso = get_object_or_404(RSO, name=rso_name)
    rso_id = RSO.objects.get(name=rso_name).id
    all_events = RSO.objects.raw('SELECT * FROM "events_event" WHERE rso_id = {}'.format(rso_id))
    return render(request, 'event_list.html', {'all_events' : all_events, 'rso' : rso})
