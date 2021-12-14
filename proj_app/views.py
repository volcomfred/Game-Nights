from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
import bcrypt

def index(request):
    request.session.flush()
    return render(request, 'index.html')


def register(request):  
    if request.method == "POST":
        errors = User.objects.reg_validator(request.POST)
        if len(errors) != 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')
        
        hashed_pw = bcrypt.hashpw(
            request.POST['password'].encode(), bcrypt.gensalt()).decode()
        
        new_user = User.objects.create(
            first_name=request.POST['first_name'], last_name=request.POST[
                'last_name'], email=request.POST['email'], password=hashed_pw
        )
        
        request.session['user_id'] = new_user.id
        return redirect('/games')
    return redirect('/')

def login(request):
    if request.method == "POST":
        errors = User.objects.login_validator(request.POST)
        if len(errors) != 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')
        this_user = User.objects.filter(email=request.POST['email'])
        request.session['user_id'] = this_user[0].id
        return redirect('/games')
    return redirect('/')

def logout(request):
    request.session.flush()
    return redirect('/')

def games(request):
    if 'user_id' not in request.session:
        return redirect('/')
    this_user = User.objects.filter(id=request.session['user_id'])
    context = {
        'user': this_user[0],
        'all_games' : Game.objects.all(),
        'user_games' : User.objects.get(id=request.session['user_id']).joined_game.all()
    }
    return render(request, 'games.html', context)

def addgame(request):
    return render(request, 'new.html')

def create(request):

    errors=Game.objects.basic_validator(request.POST)
    if len(errors)>0:
        for key,value in errors.items():
            messages.error(request, value)
        return redirect('/addgame/new')

    newgame = Game.objects.create(
        game = request.POST['game'],
        location = request.POST['location'],
        date = request.POST['date'],
        time = request.POST['time'],
        creator = User.objects.get(id=request.session['user_id']),
    )
    user = User.objects.get(id=request.session['user_id'])
    game = Game.objects.get(id=newgame.id)
    user.joined_game.add(game)
    return redirect('/games')

def game(request, game_id):
    one_game = Game.objects.get(id=game_id)
    context = {
        'game': one_game,
        'user_games' : User.objects.get(id=request.session['user_id']).joined_game.all(),
    }
    return render(request, 'game.html', context)

def delete(request, game_id):
    to_delete = Game.objects.get(id=game_id)
    to_delete.delete()
    
    return redirect('/games')

def join(request):
    user = User.objects.get(id=request.session['user_id'])
    # user = User.objects.get(id=request.session['user_id'])
    # user.joined_game.add(game)

    return redirect('/games')

def joined(request, game_id):
    user = User.objects.get(id=request.session['user_id'])
    game = Game.objects.get(id=game_id)
    user.joined_game.add(game)

    return redirect('/games')

def cancel(request, game_id):
    user = User.objects.get(id=request.session['user_id'])
    game = Game.objects.get(id=game_id)
    user.joined_game.remove(game)

    return redirect('/games')