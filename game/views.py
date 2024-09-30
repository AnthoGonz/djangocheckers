from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import Game, Piece

from .forms import GameForm,DeleteForm,CreateForm

# Create your views here.

def index(request):
     context ={}
     context['form']= GameForm()
     context['new']= CreateForm()
     return render(request, "game/menu.html",context)


##Main function to load the game. This is called everytime a move is made.
def loadGame (request):
     context ={}
     context['form']= GameForm()

     color_turn = {0:"red",
                   1:"blue"}
     player = "red"
     if request.method == "POST":
          
          gameForm = GameForm(request.POST)
          
          current_game = None

          ##Check to see if the game is being loaded via gameCode or gameID
          if(len(gameForm["game"].value()) == 0):
               if (Game.objects.filter(gameCode = gameForm['gameCode'].value()).exists() == False):
                    return render (request,"game/notexist.html")
               current_game = Game.objects.get(gameCode = gameForm["gameCode"].value())
          else:
               current_game = Game.objects.get(pk = gameForm["game"].value())



          ##Updates flipBoard value based
          current_game.flipBoard = gameForm["flipBoard"].value()
          current_game.save()

          ##Deletes all the pieces if it is a double jump
          delete_temp = request.POST.get('piecesToDelete')
          delete_temp = delete_temp.split("#")
          del delete_temp[-1]

          delete_array = []

          for o in delete_temp:
               delete_array.append([int(o[0]),int(o[1])])

          ##Checks who the current player is (used for multiplayer)
          if request.user.id == current_game.playerRed_id or request.user.id == current_game.playerBlue_id:
               if request.user != current_game.playerRed_id:
                    player = "blue"
          elif current_game.playerRed_id == None:
               if current_game.currentTurn == 0:
                    player = "red"
               elif current_game.currentTurn == 1:
                    player = "blue"

          ##Updates move if a move is made
          if gameForm["currentPositionX"].value() != "":
               form_x = int(gameForm["currentPositionX"].value())
               form_y = int(gameForm["currentPositionY"].value())

               move_x = int(gameForm["nextPositionX"].value())
               move_y = int(gameForm["nextPositionY"].value())

               piece_to_move = Piece.objects.filter(x=form_x,y=form_y, game=current_game)

               ##Changes turn if a move was made
               if current_game.currentTurn == 0:
                    current_game.currentTurn = 1
               elif current_game.currentTurn == 1:
                    current_game.currentTurn = 0; 
               current_game.save()

               ##Updates pieces to King if it is a king
               if piece_to_move[0].color == 0 and piece_to_move[0].y == 8 and piece_to_move[0].isKing != 0:
                    piece_to_move.update(isKing = 1)
               if piece_to_move[0].color == 1 and piece_to_move[0].y == 1 and piece_to_move[0].isKing != 0:
                    piece_to_move.update(isKing = 1)

               ##If it is not a double jump, check move and delete the piece if it jumped a piece
               if len(delete_array) == 0:
                    if checkMove(piece_to_move[0],[move_x,move_y],current_game):
                         piece_to_move.update(x=move_x,y=move_y)
               elif len(delete_array) != 0:
                    piece_to_move.update(x=move_x,y=move_y)


          piecesQuery = Piece.objects.all().filter(game=current_game)

          for p in piecesQuery:
               if (p.color == 0 and p.y == 8) or (p.color == 1 and p.y == 1):
                    p.isKing = 1
                    p.save()

          for a in delete_array:
               if (Piece.objects.filter(x=a[0],y=a[1],game=current_game).exists()):
                    Piece.objects.filter(x=a[0],y=a[1],game=current_game).delete()

          piecesQuery = Piece.objects.all().filter(game=current_game)

          pieces = []

          for i in piecesQuery:
               cur = []
               cur.append(i.x)
               cur.append(i.y)
               cur.append(i.color)
               cur.append(i.isKing)

               pieces.append(cur)

          return render(request,"game/pass.html",{"pieces" : pieces, "form" : GameForm(), "deleteForm" : DeleteForm(), "game" : current_game.pk,"turn": color_turn[current_game.currentTurn], "current_player" :  player, "flip_board": current_game.flipBoard,"gameCode" : current_game.gameCode})
     else:
          return render(request, "game/menu.html")


##Function used to check if the move is valid
def checkMove(curr, next, game):
    
    delete = []
    roc = abs(curr.x - next[0]) / abs(curr.y - next[1])
    dist = abs(curr.x - next[0])

    ##Conditions defined for a valid move
    if roc == 1:
     if Piece.objects.filter(x=next[0],y=next[1],game=game).exists():
          return False
     elif dist > 1 and dist % 2 != 0:
          return False
     elif dist > 1 and dist % 2 == 0:

          x_change = (next[0] - curr.x) / abs(next[0] - curr.x)
          y_change = (next[1] - curr.y) / abs(next[1] - curr.y)

          for i in range(1,dist,2):
               check_x = curr.x + (i * x_change)
               check_y = curr.y + (i * y_change)

               if (Piece.objects.filter(x=check_x,y=check_y,game=game).exists()):
                    delete.append(Piece.objects.filter(x=check_x,y=check_y,game=game))
               else:
                    return False
               
          print (delete)
          for i in delete:
               i.delete()

          return True
     else:
          return True

##View used to create a new game   
def createGame(request):
     pieces = [
          [1,1,0,0],
          [3,1,0,0],
          [5,1,0,0],
          [7,1,0,0],
          [2,2,0,0],
          [4,2,0,0],
          [6,2,0,0],
          [8,2,0,0],
          [1,3,0,0],
          [3,3,0,0],
          [5,3,0,0],
          [7,3,0,0],
          [2,6,1,0],
          [4,6,1,0],
          [6,6,1,0],
          [8,6,1,0],
          [1,7,1,0],
          [3,7,1,0],
          [5,7,1,0],
          [7,7,1,0],
          [2,8,1,0],
          [4,8,1,0],
          [6,8,1,0],
          [8,8,1,0]
     ]

     if request.method == "POST":

          gameForm = CreateForm(request.POST)

          color_turn = {0:"red",
                   1:"blue"}
          if Game.objects.filter(gameCode = gameForm['gameCodeCreate'].value()).exists():
               return render (request,"game/exists.html")
          
          game_instance = Game.objects.create()
          game_instance.gameCode = gameForm['gameCodeCreate'].value()
          game_instance.currentTurn = 0
          game_instance.save()

          player = "blue"

          for piece in pieces:
               piece_instance = Piece.objects.create(x=piece[0],y=piece[1],color=piece[2],game=game_instance)
               piece_instance.save()

          piecesQuery = Piece.objects.all().filter(game=game_instance)

          pieces = []

          for i in piecesQuery:
               cur = []
               cur.append(i.x)
               cur.append(i.y)
               cur.append(i.color)
               cur.append(i.isKing)

               pieces.append(cur)

          print (game_instance.pk)

          return render(request,"game/pass.html",{"pieces" : pieces, "form" : GameForm(), "deleteForm" : DeleteForm(),"game" : game_instance.pk,"turn": color_turn[game_instance.currentTurn], "current_player" :  player})
     else:
          return render(request, "game/index.html")

##View used to delete a game    
def deleteGame(request):
     gameForm = DeleteForm(request.POST)
     current_game = Game.objects.get(pk = gameForm["gameDelete"].value())
     current_game.delete()

     response = redirect('/')
     return response

##Tutorial View
def tutorial(request):
     return render(request, "game/tutorial.html")

#About View
def about(request):
     return render(request, "game/about.html")