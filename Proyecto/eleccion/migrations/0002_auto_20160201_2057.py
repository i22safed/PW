# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('eleccion', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='circunscripcion',
            name='escanos',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='circunscripcion',
            name='nombre',
            field=models.CharField(default=b'Circunscripcion', max_length=128),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='mesa',
            name='nombre',
            field=models.CharField(default=b'Mesa', max_length=128),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='partido',
            name='nombre',
            field=models.CharField(default=b'Partido', unique=True, max_length=128),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='resultado',
            name='valor',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
    ]
