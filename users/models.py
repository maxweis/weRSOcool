from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.files.uploadedfile import InMemoryUploadedFile
from PIL import Image
from io import BytesIO
import sys

MAX_IMAGE_WIDTH = 160
MAX_IMAGE_HEIGHT = 160

class Member(AbstractUser):
    ACAD_YEAR_CHOICES = (
            ('FR', 'Freshman'),
            ('SO', 'Sophomore'),
            ('JR', 'Junior'),
            ('SR', 'Senior'),
            ('GR', 'Graduate')
    )

    username = models.CharField(max_length=64, primary_key=True)
    academic_year = models.CharField(max_length=20, choices=ACAD_YEAR_CHOICES)
    major = models.CharField(max_length=30)
    resume = models.FileField(upload_to='member_resumes/', blank=True, null=True)
    icon = models.ImageField(upload_to='member_images/', default='default_user.png')

    def __str__(self):
        return self.first_name + self.last_name

    def save(self, *args, **kwargs):
        if self.icon:
            thumbnail = Image.open(self.icon)
            thumbnail.thumbnail((MAX_IMAGE_WIDTH, MAX_IMAGE_HEIGHT), Image.ANTIALIAS)
            thumbnail_file = BytesIO()
            thumbnail.save(thumbnail_file, "PNG")
            thumbnail_file.seek(0)
            self.icon = InMemoryUploadedFile(thumbnail_file, 'ImageField', "{}.png".format(self.icon.name.split(".")[0]), 'image/png', sys.getsizeof(thumbnail_file), None)
        super(Member, self).save(*args, **kwargs)
