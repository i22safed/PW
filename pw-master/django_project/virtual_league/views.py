from django.shortcuts import render, redirect
from virtual_league.models import TotalScore, Player
import os
from django.contrib.auth.models import User

# Create your views here.

def squad(request):
    if request.user.is_authenticated() and not request.user.userprofile.game is None:
        for player in request.user.userprofile.players.all():
            player.face = os.path.basename(player.face.url)
            player.save()
        return render(request, 'squad.html', {'players': request.user.userprofile.players.all().order_by('position')})
    else:
        return redirect('/')

def table(request):
    if request.user.is_authenticated() and not request.user.userprofile.game is None:
        totalscores = []
        for userprofile in request.user.userprofile.game.userprofile_set.all():
            totalscore = TotalScore()
            totalscore.username = userprofile.user.username
            totalscore.score = 0
            for player in userprofile.players.all():
                for playerscore in player.playerscore_set.all():
                    totalscore.score += playerscore.score
            totalscores.append(totalscore)
            totalscores.sort(key = lambda totalscore: totalscore.score, reverse=True)
        return render(request, 'table.html', {'totalscores': totalscores})
    else:
        return redirect('/')

def user(request, username):
    if request.user.is_authenticated() and not request.user.userprofile.game is None:
        if User.objects.filter(username=username).exists() and User.objects.get(username=username).userprofile.game == request.user.userprofile.game:
            return render(request, 'user.html', {'user': User.objects.get(username=username), 'players': User.objects.get(username=username).userprofile.players.all().order_by('position')})
        else:
            return render(request, 'notfound.html')
    else:
        return redirect('/')

def player(request, playername):
    if request.user.is_authenticated() and not request.user.userprofile.game is None:
        if Player.objects.filter(name=playername).exists():
            return render(request, 'player.html', {'player': Player.objects.get(name=playername)})
        else:
            return render(request, 'notfound.html')
    else:
        return redirect('/')
