# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-23 12:39
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Action',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='FBGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fb_group_id', models.CharField(max_length=50)),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Moderation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.IntegerField(choices=[(1, 'comment'), (2, 'post')])),
                ('fb_id', models.CharField(max_length=50)),
                ('fb_user_id', models.CharField(max_length=50)),
                ('text', models.TextField()),
                ('img', models.ImageField(upload_to='')),
                ('posted_at', models.DateTimeField()),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='moderations.FBGroup')),
            ],
        ),
        migrations.CreateModel(
            name='Moderator',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fb_user_id', models.CharField(max_length=50)),
                ('registered_at', models.DateTimeField()),
            ],
        ),
    ]
