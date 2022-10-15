from django.urls import path

from . import views

urlpatterns = [
    path("", views.index),
    path("estados/", views.EstadoListView.as_view()),
]
