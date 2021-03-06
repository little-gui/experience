# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-23 22:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Follower',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('follower_id', models.CharField(max_length=50)),
                ('followers', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='RetweetUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('screen_name', models.CharField(max_length=255)),
            ],
        ),
    ]
