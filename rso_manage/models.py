from django.db import models
from django.core.files.base import ContentFile
from django.core.files.uploadedfile import InMemoryUploadedFile
from users.models import Member
from PIL import Image
from io import BytesIO
import sys

MAX_IMAGE_WIDTH = 1200
MAX_IMAGE_HEIGHT = 400

class RSO(models.Model):
    name = models.CharField(max_length=100)
    date_established = models.DateField()
    college_association = models.CharField(max_length=50)
    icon = models.ImageField(upload_to='rso_icons/', default='default_rso.png')
    # creator = models.CharField(max_length=64)
    description = models.CharField(max_length=1024)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.icon:
            thumbnail = Image.open(self.icon)
            thumbnail.thumbnail((MAX_IMAGE_WIDTH, MAX_IMAGE_HEIGHT), Image.ANTIALIAS)
            thumbnail_file = BytesIO()
            thumbnail.save(thumbnail_file, "PNG")
            thumbnail_file.seek(0)
            self.icon = InMemoryUploadedFile(thumbnail_file, 'ImageField', "{}.png".format(self.icon.name.split(".")[0]), 'image/png', sys.getsizeof(thumbnail_file), None)
        super(RSO, self).save(*args, **kwargs)

class Registrations(models.Model):
    member = models.ForeignKey(Member, on_delete=models.PROTECT)
    rso = models.ForeignKey(RSO, on_delete=models.PROTECT)
    admin = models.BooleanField(default=False)

    def __str__(self):
        if self.admin:
            return self.rso.name + ': ' + self.member.username + "*"
        return self.rso.name + ': ' + self.member.username


class Tag(models.Model):
    tag = models.CharField(max_length=100)
    rso = models.ForeignKey(RSO, on_delete=models.PROTECT)

    def __str__(self):
        return self.rso.name + ": " + self.tag

    def save(self, *args, **kwargs):
        self.tag = self.tag.lower()
        return super(Tag, self).save(*args, **kwargs)

# TODO: GET RID OF THIS #
class MajorDist(models.Model):
    major = models.CharField(max_length=100)
    count = models.IntegerField()

    def __str__(self):
        return self.major + ": " + self.count
