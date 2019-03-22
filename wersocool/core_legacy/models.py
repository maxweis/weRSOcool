from django.db import models
from django.contrib.auth.models import User

class InvolvedWith(models.Model):
    member_netId = models.ForeignKey(Member, on_delete=models.CASCADE)
    rso_name = models.ForeignKey(RSO, on_delete=models.CASCADE)
    role = models.CharField(max_length=80)
    semesters_involved = models.IntegerField()

    class Meta:
        unique_together = (("member_netId", "rso_name"))

class MeetingEvent(models.Model):
    name = models.CharField(max_length=100)
    date_time = models.DateTimeField()
    rso_name = models.ForeignKey(RSO, on_delete=models.CASCADE)

    class Meta:
        unique_together = (("name", "rso_name"))

class Attends(models.Model):
    member_netId = models.ForeignKey(Member, on_delete=models.CASCADE)
    meeting_name = models.ForeignKey(MeetingEvent, on_delete=models.CASCADE)
    rso_name = models.ForeignKey(RSO, on_delete=models.CASCADE)
