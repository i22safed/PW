# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Anuncio',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('titulo', models.CharField(max_length=50)),
                ('fecha', models.DateTimeField(default=datetime.datetime.now)),
                ('texto', models.TextField(max_length=200)),
                ('cambio', models.TextField(max_length=200)),
                ('imagen', models.ImageField(upload_to=b'imgAnuncios', verbose_name=b'Imagen', blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Categoria',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(unique=True, max_length=50)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Comentario',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('texto', models.TextField(help_text=b'Comenta...', max_length=200, verbose_name=b'Comentario')),
                ('fecha', models.DateTimeField(default=datetime.datetime.now)),
                ('anuncio', models.ForeignKey(to='wajosh.Anuncio')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Distribucion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('correo', models.EmailField(max_length=75)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Mensaje',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fecha', models.DateTimeField(default=datetime.datetime.now)),
                ('texto', models.TextField()),
                ('leido', models.BooleanField(default=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Provincia',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(unique=True, max_length=50)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('user_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('avatar', models.ImageField(upload_to=b'imgProfiles', verbose_name=b'Imagen', blank=True)),
                ('ciudad', models.CharField(max_length=50, blank=True)),
                ('provincia', models.ForeignKey(to='wajosh.Provincia')),
            ],
            options={
                'abstract': False,
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
            },
            bases=('auth.user',),
        ),
        migrations.AddField(
            model_name='mensaje',
            name='fromu',
            field=models.ForeignKey(related_name='fromu', blank=True, to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='mensaje',
            name='to',
            field=models.ForeignKey(related_name='to', blank=True, to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='comentario',
            name='propietario',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='anuncio',
            name='categoria',
            field=models.ForeignKey(to='wajosh.Categoria'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='anuncio',
            name='propietario',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='anuncio',
            name='provincia',
            field=models.ForeignKey(to='wajosh.Provincia'),
            preserve_default=True,
        ),
    ]
