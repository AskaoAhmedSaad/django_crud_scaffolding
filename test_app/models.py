from django.db import models
from django.utils import timezone


class Option(models.Model):
    name = models.CharField(max_length=255,null=False, blank=False)
    value = models.CharField(max_length=255, null=False, blank=False)
    created = models.DateTimeField(default=timezone.now(), null=False, blank=False)


class UserOption(models.Model):
    name = models.CharField(max_length=255,null=False, blank=False)
    option = models.ForeignKey(Option) # every user has option
    created = models.DateTimeField(default=timezone.now(), null=False, blank=False)
