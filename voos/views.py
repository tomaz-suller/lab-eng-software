from django.shortcuts import render
from django.views.generic import ListView
from django.views.generic.edit import CreateView

from .models import Estado, CompanhiaAerea
from .forms import CompanhiaAereaForm


class EstadoListView(ListView):
    model = Estado
    context_object_name = "estado_list"


class CompanhiaAereaListView(ListView):
    model = CompanhiaAerea
    context_object_name = "companhia_aerea_list"


class CompanhiaAereaCreateView(CreateView):
    model = CompanhiaAerea
    # fields = ['nome', 'sigla']
    form_class = CompanhiaAereaForm
    success_url = '/crud/companhia-aerea'


def index(request):
    context = {
        "base_pages": ["crud", "movimentacao", "relatorio"],
    }
    return render(request, "voos/index.html", context)

def inicio(request):
    return render(request, "voos/inicio.html")

def crud(request):
    return render(request, "voos/crud.html")

def movimentacao(request):
    return render(request, "voos/movimentacao.html")

def relatorio(request):
    return render(request, "voos/relatorio.html")

