from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.forms import UserCreationForm
from authentication.forms import Signup as SignupForm
from django.contrib.auth.models import User
from virtual_league.models import UserProfile, Game, Player
from virtual_league.forms import NewGame as NewGameForm
import random

# Create your views here.

def index(request):
    if request.user.is_authenticated():
        if request.user.userprofile.game is None:
            if request.method == 'POST':
                if request.POST.get('joingame') == "":
                    return render(request, 'joingame.html', {'games': Game.objects.all()})
                elif request.POST.get('newgame') == "":
                    return render(request, 'newgame.html')
                elif request.POST.get('create') == "":
                    form = NewGameForm(request.POST)
                    if form.is_valid():
                        game = Game()
                        game.name = request.POST['name']
                        game.key = request.POST['key']
                        if Game.objects.filter(name=game.name).exists():
                            return render(request, 'newgame.html', {'errors': True})
                        game.save()
                        request.user.userprofile.game = game
                        for i in range(1, 8):
                            player = random.choice(Player.objects.filter(position = i))
                            request.user.userprofile.players.add(player)
                        request.user.userprofile.save()
                        return redirect('/')
                    else:
                        return render(request, 'newgame.html')
                elif request.POST.get('join') == "":
                    if 'gamename' not in request.POST:
                        return render(request, 'joingame.html', {'games': Game.objects.all()})
                    else:
                        if Game.objects.get(name=request.POST['gamename']).userprofile_set.count() > 4:
                            return render(request, 'joingame.html', {'games': Game.objects.all(), 'error': "maxusers"})
                        gamekey = request.POST['gamename'] + "key"
                        if not Game.objects.filter(name=request.POST['gamename'], key=request.POST[gamekey]).exists():
                            return render(request, 'joingame.html', {'games': Game.objects.all(), 'error': "key"})
                        else:
                            for i in range(1, 8):
                                players = Player.objects.filter(position=i)
                                request.user.userprofile.game = Game.objects.get(name=request.POST['gamename'])
                                for user in Game.objects.get(name=request.POST['gamename']).userprofile_set.all():
                                    players = players.exclude(name=user.players.get(position=i).name)
                                player = random.choice(players)
                                request.user.userprofile.players.add(player)
                            request.user.userprofile.save()
                            return redirect('/')
                else:
                    return redirect('/')
            else:
                return render(request, 'start.html')
        else:
            return render(request, 'home.html')
    else:
        if request.method == 'GET':
            return render(request, 'index.html')
        elif request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    auth_login(request, user)
                    return redirect('/')
                else:
                    return render(request, 'disabledaccount.html')
            else:
                return render(request, 'index.html', {'errors': True})

def logout(request):
    if request.user.is_authenticated():
        auth_logout(request)
    return redirect('/')

def signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html')
    elif request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form = SignupForm(request.POST)
            if form.is_valid():
                username = request.POST['username']
                email = request.POST['email']
                password = request.POST['password1']
                user = User.objects.create_user(username, email, password)
                if request.POST['first_name']:
                    user.first_name = request.POST['first_name']
                if request.POST['last_name']:
                    user.last_name = request.POST['last_name']
                user.save()
                userProfile = UserProfile()
                userProfile.user = user
                userProfile.save()
                user = authenticate(username=username, password=password)
                auth_login(request, user)
                return redirect('/')
            else:
                return render(request, 'signup.html', {'errors': True})
        else:
            return render(request, 'signup.html', {'errors': True})
