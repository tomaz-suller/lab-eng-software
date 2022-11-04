from django.urls import path

from . import views

urlpatterns = [
    path("", views.index),
    path("crud/", views.crud),
    path("movimentacao/", views.movimentacao),
    path("relatorio/", views.relatorio),
    path("estados/", views.EstadoListView.as_view()),
    path("inicio/", views.inicio),
    path("inicio/crud/", views.crud),
    path("inicio/movimentacao/", views.movimentacao),
    path("inicio/relatorio/", views.relatorio),

    path("crud/companhia-aerea/criar", views.CompanhiaAereaCreateView.as_view()),
    path("crud/companhia-aerea", views.CompanhiaAereaListView.as_view()),
    path("crud/companhia-aerea/update/<int:pk>", views.CompanhiaAereaUpdateView.as_view()),
]
