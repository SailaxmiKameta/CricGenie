# players/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.search_players, name='search_players'),
    path('player/details/<int:player_id>/', views.player_details, name='player_details'),
]