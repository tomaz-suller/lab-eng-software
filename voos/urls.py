from django.urls import path

from . import views

urlpatterns = [
    path("", views.index),
    path("crud/", views.crud),
    path("movimentacao/", views.movimentacao),
    path("relatorio/", views.relatorio),
    path("relatorio/relatorio-partidas-chegadas", views.relatorio_partidas_chegadas),
    path("relatorio/relatorio-movimentacoes", views.relatorio_movimentacoes),
    path("estados/", views.EstadoListView.as_view()),

    path("movimentacao/atualizar/<int:pk>", views.movimentacao_detail),
    path("movimentacao/atualizar/confirmado", views.movimentacao_confirmado),

    path("crud/companhia-aerea/criar", views.CompanhiaAereaCreateView.as_view()),
    path("crud/companhia-aerea", views.CompanhiaAereaListView.as_view()),
    path("crud/companhia-aerea/update/<int:pk>", views.CompanhiaAereaUpdateView.as_view()),
]
