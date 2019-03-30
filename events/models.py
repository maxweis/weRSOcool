from django.db import models
from rso_manage.models import RSO
from users.models import Member

class Event(models.Model):
    name = models.CharField(max_length=64);
    rso = models.ForeignKey(RSO, on_delete=models.PROTECT)
    time_begin = models.DateTimeField()
    time_end = models.DateTimeField()
    place = models.CharField(max_length=64);

class Attending(models.Model):
    user = models.ForeignKey(Member, on_delete=models.PROTECT)
    event = models.ForeignKey(Event, on_delete=models.PROTECT)
