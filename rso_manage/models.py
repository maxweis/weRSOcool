from django.db import models
from users.models import Member

class RSO(models.Model):
    name = models.CharField(max_length=100)
    date_established = models.DateField()
    college_association = models.CharField(max_length=50)
    icon = models.ImageField()
    creator = models.OneToOneField(Member, models.CASCADE)

    def __str__(self):
        return self.name
