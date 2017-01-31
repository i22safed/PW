# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('eleccion', '0002_auto_20160201_2057'),
    ]

    operations = [
        migrations.RenameField(
            model_name='resultado',
            old_name='valor',
            new_name='votos',
        ),
    ]
