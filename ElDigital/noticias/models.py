# -*- coding: utf-8 -*-

from django.db import models
from django.utils import timezone

# Create your models here.


class Post(models.Model):

    id_post = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    body = models.TextField()
    tag = models.TextField()
    user = models.ForeignKey('auth.User')
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(auto_now=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __unicode__(self):
        return self.title

class Comentario(models.Model):
    id_coment = models.AutoField(primary_key=True)
    user = models.ForeignKey('auth.User')
    title = models.CharField(max_length=200)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.title

    #class Meta:
        #ordering = ["-created"]

class Mensaje(models.Model):
    id_mensaje=models.AutoField(primary_key=True)
    user = models.ForeignKey('auth.User')
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=200)
    body = models.TextField()

    def __unicode__(self):
        return self.title
