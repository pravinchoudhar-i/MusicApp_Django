from django.db import models
# from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import User
import datetime

class AddSong(models.Model):
	status_code = models.BooleanField(default=1)
	song_name = models.CharField(max_length=200, blank=True, null=True)
	artist = models.CharField(max_length=200, blank=True, null=True)
	genre = models.CharField(max_length=200, blank=True, null=True)
	release_year = models.IntegerField(default=100, blank=True, null=True)
	song_file = models.FileField(upload_to='Music_file',blank=True, null=True)
	add_to_like = models.BooleanField(default=1, blank=True, null=True)
	
class CreateList(models.Model):
    list_name = models.models.CharField( max_length=200, blank=True , null=True)