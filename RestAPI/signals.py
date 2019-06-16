
import os
from datetime import timedelta

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Event

@receiver(post_save, sender=Event)
def update_actor(sender, instance, **kwargs):

    actor = instance.actor
    event_day = instance.created_at.day
    actor_previous_ts = actor.latest_event_ts

    # update actor event_count and latest_event_ts
    actor.event_count = actor.event_set.count()
    actor.latest_event_ts = instance.created_at

    try:
        actor_previous_event_day = actor_previous_ts.day
    except AttributeError:
        # set it one day back from the event
        actor_previous_event_day = event_day - 1

    if event_day == (actor_previous_event_day + 1):
        actor.streak = actor.streak + 1
    else:
        pass

    actor.save(update_fields=['streak', 'event_count', 'latest_event_ts'])
