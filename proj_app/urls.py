from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('login', views.login),
    path('logout', views.logout),
    path('games', views.games),
    path('edit/<int:user_id>', views.edit),
    path('addgame/new', views.addgame),
    path('game/<int:game_id>', views.game),
    path('addgame/create', views.create),
    path('games/<int:game_id>/delete', views.delete),
    path('games/<int:game_id>/cancel', views.cancel),
    path('games/<int:game_id>/joined', views.joined),
]