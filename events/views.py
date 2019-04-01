from django.shortcuts import render, redirect, get_object_or_404
from .forms import EventCreationForm
from rso_manage.models import RSO
from events.models import Event, Attending
from users.models import Member

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
    return render(request, 'event_list.html', {'all_events' : all_events, 'rso' : rso, 'attend' : Attending.objects.all()})

def attend_event(request, rso_name, event):
    event = Event.objects.get(name=event)
    username = request.user.username
    member = Member.objects.get(username=username)
    if not Attending.objects.filter(user=member, event=event).exists():
        attendance = Attending(user=member, event=event)
        attendance.save()
    return redirect('/rsos/'+rso_name+'/events')


def event_statistics(request, rso_name):
    #WIP
    rso = get_object_or_404(RSO, name=rso_name)
    rso_id = RSO.objects.get(name=rso_name).id
    all_events = RSO.objects.raw('SELECT * FROM "events_event" WHERE rso_id = {}'.format(rso_id))
    attendance = RSO.objects.raw('SELECT id, name, count(user_id) FROM "events_event", "events_attending" WHERE rso_id = {} Group By name '.format(rso_id))
# list(RSO.objects.raw('SELECT events_event.id, name, count(user_id) FROM "events_event", "events_attending" Group By name '))
    print(attendance)
    return None
    
