# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_auto_20160209_1841'),
    ]

    operations = [
        migrations.AlterField(
            model_name='articulo',
            name='texto',
            field=models.CharField(max_length=2000),
            preserve_default=True,
        ),
    ]
