from django.urls import path

from . import views

urlpatterns = [
    path("", views.index),
    path("crud/", views.crud),
    path("movimentacao/", views.movimentacao),
    path("relatorio/", views.relatorio),
    path("estados/", views.EstadoListView.as_view()),
]
