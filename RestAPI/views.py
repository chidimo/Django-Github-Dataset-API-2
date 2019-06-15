# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import pytz
from dateutil.parser import parse
from dateutil.tz import gettz

from django.db import IntegrityError

from django.http import Http404, HttpResponse
from django.shortcuts import redirect
from django.utils import timezone
from django.conf import settings

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .serializers import ActorSerializer, RepoSerializer, EventSerializer
from .models import Actor, Repo, Event


class RepoViewSet(viewsets.ModelViewSet):
    """Docstring"""
    queryset = Repo.objects.all()
    serializer_class = RepoSerializer

def create_events_data(data):
    event_id = int(data["id"])
    event_type = data["type"]
    parsed_date = parse(data["created_at"])
    created_at = timezone.make_aware(parsed_date, gettz('Africa/Abidjan'))

    actor = data["actor"]
    actor_id = int(actor["id"])
    login = actor["login"]
    avatar_url = actor["avatar_url"]

    repo = data["repo"]
    repo_id = int(repo["id"])
    repo_name = repo["name"]
    repo_url = repo["url"]

    act, created = Actor.objects.get_or_create(id=actor_id, login=login, avatar_url=avatar_url)
    rep, _ = Repo.objects.get_or_create(id=repo_id, name=repo_name, url=repo_url)
    event, created = Event.objects.get_or_create(id=event_id, type=event_type, actor=act, repo=rep, created_at=created_at)
    if created:
        return ('Object created', 201)
    return ('Event already exists', 400)


class EventViewSet(viewsets.ModelViewSet):
    """Docstring"""
    queryset = Event.objects.all()
    serializer_class = EventSerializer

    def create(self, request):
        if request.method == 'POST':
            data = request.data
            message, status = create_events_data(data)
            return HttpResponse(message, status=status)    


@api_view(['GET', 'DELETE'])
def erase_all_events(request):
    e = Event.objects.all()
    n = e.count()
    e.delete()
    return Response({'erase' : 'Deleted {} events'.format(n)})


@api_view(['GET', 'PUT'])
def actors_index(request):
    if request.method == 'GET':
        actors = []
        for actor in Actor.objects.all():
            serialized_actor = ActorSerializer(actor)
            actors.append(serialized_actor.data)
        return Response(actors)

    if request.method == 'PUT':
        data = request.data
        actor_id = data["id"]
        login = data["login"]
        avatar_url = data["avatar_url"]
        try:
            actor = Actor.objects.get(id=actor_id)
            actor.avatar_url = avatar_url # update the avatar_url

            if actor.login != login: # if the login has changed, return 400
                actor.login = login
                status = 400
            else:
                status = 200
            actor.save()
            return HttpResponse("Actor avatar_url updated successfully", status=status)
        except Actor.DoesNotExist:
            raise Http404("Actor does not exist")


@api_view(['GET', 'POST'])
def actor_events(request, id):
    try:
        actor = Actor.objects.get(id=int(id))
        actor_events = Event.objects.filter(actor__id=int(id))
        data = []
        for event in actor_events:
            serialized_event = EventSerializer(event)
            data.append(serialized_event.data)
        return Response(data)
    except Actor.DoesNotExist:
        raise Http404("Actor does not exist")


@api_view(['GET', 'POST'])
def actors_by_streak(request):
    if request.method == 'GET':
        actors = []
        for actor in Actor.objects.all().order_by('-streak', '-latest_event_timestamp', 'login'):
            serialized_actor = ActorSerializer(actor)
            actors.append(serialized_actor.data)
        return Response(actors)
