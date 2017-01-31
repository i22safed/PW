# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='articulo',
            name='fecha',
            field=models.DateField(default=datetime.date.today),
            preserve_default=True,
        ),
    ]
