from django.db import models

class RSO(models.Model):
    name = models.CharField(max_length=100)
    year_established = models.IntegerField()
    college_association = models.CharField(max_length=50)
    icon = models.ImageField()
