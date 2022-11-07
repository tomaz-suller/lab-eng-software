from django.urls import path

from . import views

urlpatterns = [
    path("", views.index),
    path("crud", views.crud),
    path("movimentacao", views.movimentacao),
    path("relatorio", views.relatorio),
    path("relatorio/partidas-chegadas", views.relatorio_partidas_chegadas),
    path("relatorio/movimentacoes", views.relatorio_movimentacoes),
    path("movimentacao/atualizar/<int:pk>", views.InstanciaVooUpdateView.as_view()),
]

MODEL_ENDPOINTS = (
    "companhia-aerea",
    "voo",
    "instancia-voo",
)

for model_endpoint in MODEL_ENDPOINTS:
    model_class_name = "".join(word.title() for word in model_endpoint.split("-"))
    urlpatterns.extend(
        (
            path(
                f"crud/{model_endpoint}/criar",
                getattr(views, f"{model_class_name}CreateView").as_view(),
            ),
            path(
                f"crud/{model_endpoint}",
                getattr(views, f"{model_class_name}ListView").as_view(),
            ),
            path(
                f"crud/{model_endpoint}/alterar/<str:pk>",
                getattr(views, f"{model_class_name}UpdateView").as_view(),
            ),
            path(
                f"crud/{model_endpoint}/apagar/<str:pk>",
                getattr(views, f"{model_class_name}DeleteView").as_view(),
            ),
        )
    )
