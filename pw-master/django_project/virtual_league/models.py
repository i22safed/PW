from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Player(models.Model):
    name = models.CharField(max_length=50)
    POSITIONS = (
        (1, ("LW")),
        (2, ("LB")),
        (3, ("CB")),
        (4, ("P")),
        (5, ("RB")),
        (6, ("RW")),
        (7, ("G")),
    )
    position = models.IntegerField(choices=POSITIONS)
    face = models.ImageField(upload_to='virtual_league/static/images/faces', default='virtual_league/static/images/faces/default.png')

    def __str__(self):
        return self.name

class PlayerScore(models.Model):
    player = models.ForeignKey(Player)
    score = models.IntegerField()
    fixture = models.IntegerField()

class Game(models.Model):
    name = models.CharField(max_length=50)
    key = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class UserProfile(models.Model):
    # Django user
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    # Extending the existing User model
    game = models.ForeignKey(Game, null=True)
    players = models.ManyToManyField(Player)

    def __str__(self):
        return self.user.username

class TotalScore(models.Model):
    username = models.CharField(max_length=50)
    score = models.IntegerField()
