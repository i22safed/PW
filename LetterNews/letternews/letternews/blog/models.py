from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User


class Tag(models.Model):
    slug = models.SlugField(max_length=200, unique=True)

    def __unicode__(self):
        return self.slug

#class EntryQuerySet(models.QuerySet):
    #def published(self):
        #return self.filter(publish=True)



class Entry(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    body = models.TextField()
    slug = models.SlugField(max_length=200, unique=True)
    publish = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    tags = models.ManyToManyField(Tag)
    author = models.ForeignKey(User)

   # objects = EntryQuerySet.as_manager()

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("entry_detail", kwargs={"slug": self.slug})

    class Meta:
        verbose_name = "Blog Entry"
        verbose_name_plural = "Blog Entries"
        ordering = ["-created"]
        
class Comentario(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, null=True, default=None)
    entry = models.ForeignKey(Entry)
    title = models.CharField(max_length=200)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.title

    #class Meta:
        #ordering = ["-created"]

class Mensaje(models.Model):
    id=models.AutoField(primary_key=True)
    user = models.ForeignKey(User)
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=200)
    body = models.TextField()

    def __unicode__(self):
        return self.title