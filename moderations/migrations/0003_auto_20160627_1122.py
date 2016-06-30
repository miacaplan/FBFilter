# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-27 08:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('moderations', '0002_auto_20160627_1108'),
    ]

    operations = [
        migrations.AddField(
            model_name='postment',
            name='hash_val',
            field=models.CharField(default='', max_length=64),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='postment',
            name='nesting_level',
            field=models.PositiveSmallIntegerField(default=0),
            preserve_default=False,
        ),
    ]