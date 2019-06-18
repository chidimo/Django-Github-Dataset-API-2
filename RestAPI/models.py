# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import reverse
from django.conf import settings
from django.utils import timezone

from django.db import models


class Actor(models.Model):
    id = models.IntegerField(primary_key=True)
    login = models.CharField(max_length=50)
    avatar_url = models.URLField()
    event_count = models.IntegerField(default=0)
    latest_event_ts = models.DateTimeField(null=True)
    streak = models.IntegerField(default=0)
    max_streak = models.IntegerField(default=1)


    class Meta:
        ordering = ('-event_count', '-latest_event_ts', 'login')

    def __str__(self):
        return self.login

    def actor_events_queryset(self):
        return self.event_set.all().order_by('-created_at', )

    def actor_events_url(self):
        return settings.BASE_URL + reverse('RestAPI:actor_events', args=[self.id])

class Repo(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    url = models.URLField()

    def __str__(self):
        return self.name

class Event(models.Model):
    id = models.IntegerField(primary_key=True)
    type = models.CharField(max_length=12)
    actor = models.ForeignKey(Actor, on_delete=models.CASCADE)
    repo = models.ForeignKey(Repo, on_delete=models.CASCADE)
    created_at = models.DateTimeField()

    class Meta:
        ordering = ("id", )

    def __str__(self):
        return "{}".format(self.id)
