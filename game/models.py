from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Game(models.Model):
    gameID = models.AutoField(primary_key=True)
    gameCode = models.CharField(max_length=5)
    playerRed_id = models.ForeignKey(User,related_name="red_player", on_delete=models.CASCADE,null = True,blank = True)
    playerBlue_id = models.ForeignKey(User,related_name="blue_player", on_delete=models.CASCADE, null = True,blank = True)
    currentTurn = models.IntegerField(default = 0, null = True, blank = True)
    flipBoard = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.gameID}"

class Piece (models.Model):
    color = models.IntegerField()
    x = models.IntegerField()
    y = models.IntegerField()
    game = models.ForeignKey(Game, on_delete=models.CASCADE, blank=True, null=True)
    isKing = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.game} - {self.x}, {self.y}"
