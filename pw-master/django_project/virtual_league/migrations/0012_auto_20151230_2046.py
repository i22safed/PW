# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2015-12-30 19:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('virtual_league', '0011_auto_20151230_2045'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='face',
            field=models.ImageField(default='static/images/search.png', null=True, upload_to='static/images/faces'),
        ),
    ]
