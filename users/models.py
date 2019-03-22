from django.db import models
from django.contrib.auth.models import AbstractUser

class Member(AbstractUser):
    ACAD_YEAR_CHOICES = (
            ('FR', 'Freshman'),
            ('SO', 'Sophomore'),
            ('JR', 'Junior'),
            ('SR', 'Senior'),
            ('GR', 'Graduate')
    )

    academic_year = models.CharField(max_length=20, choices=ACAD_YEAR_CHOICES)
    major = models.CharField(max_length=30)
    resume = models.FileField(upload_to='member_resumes/')
    icon = models.ImageField(upload_to='member_images/')

    def __str__(self):
        return self.first_name + self.last_name
