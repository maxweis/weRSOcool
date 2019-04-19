from django.db import models, connection
from rso_manage.models import RSO, Registrations
from users.models import Member
from datetime import datetime,date,timedelta

def sleep_times():

    sleep = []
    for i in range(20):
        now = datetime.now()
        sleeptime = datetime(now.year, now.month, now.day) + timedelta(days=i) + timedelta(hours=22)

        waketime = sleeptime + timedelta(hours=10)

        sleep.append((sleeptime, waketime))

    return sleep


    

def get_best_time(event_times):
    #event times is a list of tuples of start an dend
    event_types = {}

    
    

    for start, end in event_times:
        event_types[start] = event_types.get(start, 0) + 1
        event_types[end] = event_types.get(end, 0) - 1

    for start, end in sleep_times():
        event_types[start] = event_types.get(start, 0) + 99
        event_types[end] = event_types.get(end, 0) - 99


    # assume that people are going to need one day in advance
    today = datetime.now()
    tomorrow = datetime.now() + timedelta(days=1)
    if not event_times:
        return tomorrow, 0
    sorted_events = sorted(event_types.keys())

    times = 0
    conflicts = 0
    conflict_map = {}
    for event in sorted_events:
        conflicts += event_types[event]
        conflict_map[event] = conflicts

    


    latest_day = datetime.now() + timedelta(days=14);

    potential_days = [day for day in conflict_map.keys() if day < latest_day and day > tomorrow]

    
    best_day = min(potential_days, key = lambda x: conflict_map[x])
    num_conflicts = conflict_map[best_day]


    return best_day, num_conflicts

# gets all the events that members are in for an rso
def members_events(rso_id):
    query = 'SELECT ev.time_begin, ev.time_end FROM \
                 ((rso_manage_registrations AS reg JOIN users_member AS memb ON reg.member_id = memb.username) JOIN events_attending as att ON att.user_id = memb.username Join events_event As ev On att.event_id = ev.id) \
    WHERE reg.rso_id = {};'.format(rso_id)

    cursor = connection.cursor()
    cursor.execute(query)
    results = cursor.fetchall()

    return results
    
