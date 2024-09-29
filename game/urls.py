from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("createGame/", views.createGame, name="createGame"),
    path("loadGame/", views.loadGame, name="loadGame"),
    path("deleteGame/",views.deleteGame, name="deleteGame"),
    path("tutorial/",views.tutorial, name="tutorial"),
    path("about/",views.about,name="about")
]