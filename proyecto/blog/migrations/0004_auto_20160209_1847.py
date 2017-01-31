# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_auto_20160209_1844'),
    ]

    operations = [
        migrations.AlterField(
            model_name='articulo',
            name='texto',
            field=models.TextField(),
            preserve_default=True,
        ),
    ]
