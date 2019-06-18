import os
import datetime
from datetime import timedelta
from dateutil.relativedelta import relativedelta

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Event

@receiver(post_save, sender=Event)
def update_actor(sender, instance, **kwargs):

    actor = instance.actor
    event_time = instance.created_at
    actor_previous_ts = actor.latest_event_ts

    # update actor event_count and latest_event_ts
    actor.event_count = actor.event_set.count()
    actor.latest_event_ts = instance.created_at

    if actor_previous_ts:
        events_time_diff = relativedelta(actor_previous_ts, event_time)
        total_hours_between_events = events_time_diff.hours + (24 * events_time_diff.days)

        # if absolute number of hours between events is between 24 and 48 increase streak
        if 24 <= abs(total_hours_between_events) <= 48:
            print('*************** increase streak ******************')
            actor.streak = actor.streak + 1
        else: # reset streak
            # update max_streak before resetting streak accummulator
            print('streak ', actor.streak, ' max_streak ', actor.max_streak)
            actor.max_streak = actor.max_streak if actor.max_streak > actor.streak else actor.streak
            actor.streak = 0
    else:
        actor.streak = 0

    actor.save(update_fields=['streak', 'event_count', 'latest_event_ts'])
    print('********AFTER *********', 'streak ', actor.streak, ' max_streak ', actor.max_streak)
