# -*- coding: utf-8 -*-

from django.db import models
from django.utils import timezone

# Create your models here.

class Post(models.Model):    # model.Models → Para saber que es un modelo de Django

    author = models.ForeignKey('auth.User')     # Linka con otro modelo (?)
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank = True , null = True)
    section = models.TextField(max_length=20)
    id_post = models.TextField(max_length=8)

    def publish(self):      # Metodo de la clase Post
        self.published_date = timezone.now()
        self.save()

    def __unicode__(self):  # Importante, debe de llevar __unicode__ , no __str__
        return self.title
