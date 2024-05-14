# players/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.SearchPlayersView.as_view(), name='search_players'),
    path('player/<int:player_id>/', views.player_details, name='player_details'),
    path('player/<int:player_id>/add_remove_favorite/', views.add_remove_favorite, name='add_remove_favorite'),
    path('favorite-players/', views.favorite_players, name='favorite_players'),


]
