from django.db import models
from django.contrib.auth.models import User


class Member(models.Model):
    ACAD_YEAR_CHOICES = (
            ('FR', 'Freshman'),
            ('SO', 'Sophomore'),
            ('JR', 'Junior'),
            ('SR', 'Senior'),
            ('GR', 'Graduate')
    )

    name = models.CharField(max_length=50)
    netId = models.CharField(max_length=10, primary_key=True)
    primary_email = models.EmailField(max_length=50)
    academic_year = models.CharField(max_length=20, choices=ACAD_YEAR_CHOICES)
    major = models.CharField(max_length=30)
    resume_url = models.FileField(upload_to='member_resumes/')
    image_url = models.ImageField(upload_to='member_images/')

    user = models.OneToOneField(User, on_delete=models.CASCADE)

class RSO(models.Model):
    name = models.CharField(max_length=50, primary_key=True)
    year_established = models.IntegerField()
    college_assocation = models.CharField(max_length=50)
    picture_url = models.ImageField(upload_to='rso_images/')

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
