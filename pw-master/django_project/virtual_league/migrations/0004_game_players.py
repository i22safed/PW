# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2015-12-26 22:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('virtual_league', '0003_auto_20151226_2315'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='players',
            field=models.ManyToManyField(to='virtual_league.Player'),
        ),
    ]
