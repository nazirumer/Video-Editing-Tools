from django.db import models

from django.core.validators import FileExtensionValidator
from time import timezone
# Create your models here.

class O_Video(models.Model):
    original_video = models.FileField(upload_to='original_uploaded',null=True,
        validators=[FileExtensionValidator(allowed_extensions=['MOV','avi','mp4','webm','mkv'])])

class M_Video(models.Model):
    merged_video = models.FileField(upload_to='merged_uploaded',null=True,
        validators=[FileExtensionValidator(allowed_extensions=['MOV','avi','mp4','webm','mkv'])])
    date_uploaded = models.DateTimeField(auto_now_add=True, null=True)

""" class Scale(models.Model):
    s = (
        ('one_with_one', "One with one"),
        ('one_with_many', "One with many")
    )
    scale_type = models.CharField(max_length=20, choices=s, null=True) 

class Cut_Original(models.Model):
    cut_original = models.FileField(upload_to='cut_original',null=True)
    #v = models.CharField(max_length=10000, null=True)"""

class Zip_file(models.Model):
    file = models.FileField(upload_to='download_zip',null=True)

class Output_Video(models.Model):
    output = models.FileField(upload_to='output_video', null=True)      