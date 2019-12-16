# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.forms import ModelForm
from django.contrib.auth.models import User

from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class Hospital(models.Model):
	class Meta:
		db_table = 'hospitals'
	name = models.CharField(max_length=255, blank=True)
	location = models.CharField(max_length=255, blank=True)
	description = models.TextField(max_length=1000, blank=True)
	def __str__(self):
		return self.name

class UserProfile(models.Model):
	class Meta:
		#db_table = 'user_profile'
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	name = models.CharField(max_length=VARCHAR)
	institution = models.ForeignKey(Hospital, blank=True, null=True, on_delete=models.CASCADE)
	bio = models.TextField(max_length=1000, blank=True)
	def __str__(self):
		return self.user.username

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
	if created:
		UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
	instance.userprofile.save()
