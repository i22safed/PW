# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('eleccion', '0003_auto_20160202_1122'),
    ]

    operations = [
        migrations.CreateModel(
            name='Votos',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('partido', models.CharField(default=b'', max_length=128)),
                ('numero', models.IntegerField(default=0)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
