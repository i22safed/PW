# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_auto_20150124_0917'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comentario',
            name='user',
            field=models.ForeignKey(default=None, to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
    ]
