# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_auto_20150124_0824'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comentario',
            name='user',
            field=models.ForeignKey(default=None, blank=True, to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
