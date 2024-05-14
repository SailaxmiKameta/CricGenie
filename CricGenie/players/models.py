from django.contrib.auth.models import User
from django.db import models

class FavoritePlayer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    player_id = models.IntegerField()
    player_name = models.CharField(max_length=255, default="")  # Set your desired default value here

    def __str__(self):
        return f"{self.user.username}'s Favorite: {self.player_name}"


class PlayerForm(models.Model):
    player_name = models.CharField(max_length=100)
    player_id = models.CharField(max_length=100)

    def __str__(self):
        return self.player_name