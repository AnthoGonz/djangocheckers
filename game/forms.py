from django import forms

class GameForm(forms.Form):
    currentPositionX = forms.IntegerField(label = "Piece to Move X",required=False)
    currentPositionY = forms.IntegerField(label = "Piece to Move X",required=False)
    nextPositionX = forms.IntegerField(label = "Place to go X",required=False)
    nextPositionY = forms.IntegerField(label = "Place to go Y",required=False)
    piecesToDelete = forms.CharField(required=False)
    flipBoard = forms.BooleanField(required=False)
    gameCode = forms.CharField(max_length=5)
    game = forms.IntegerField(label = "Game ID")

class DeleteForm(forms.Form):
    gameDelete = forms.IntegerField(label = "Game Delete")

class CreateForm(forms.Form):
    gameCodeCreate = forms.CharField(max_length=5)