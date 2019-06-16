# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2019-06-16 00:49
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Actor',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('login', models.CharField(max_length=50)),
                ('avatar_url', models.URLField()),
                ('event_count', models.IntegerField(default=0)),
                ('latest_event_timestamp', models.DateTimeField(default=django.utils.timezone.now)),
                ('streak', models.IntegerField(default=0)),
                ('pushed_today', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ('-event_count', '-latest_event_timestamp', 'login'),
            },
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('type', models.CharField(max_length=12)),
                ('created_at', models.DateTimeField()),
                ('actor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='RestAPI.Actor')),
            ],
            options={
                'ordering': ('id',),
            },
        ),
        migrations.CreateModel(
            name='Repo',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('url', models.URLField()),
            ],
        ),
        migrations.AddField(
            model_name='event',
            name='repo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='RestAPI.Repo'),
        ),
    ]
