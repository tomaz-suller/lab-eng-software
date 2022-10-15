from django.shortcuts import render
from django.views.generic import ListView

from .models import Estado


class EstadoListView(ListView):
    model = Estado
    context_object_name = "estado_list"


def index(request):
    context = {
        "base_pages": ["crud", "movimentacao", "relatorio"],
    }
    return render(request, "voos/index.html", context)
