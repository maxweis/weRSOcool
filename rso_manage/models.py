from django.db import models

class RSO(models.Model):
    name = models.CharField()
    year_established = models.IntegerField()
    college_association = models.CharField()
    icon = models.ImageField()
