from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import render
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView

from .forms import CompanhiaAereaForm
from .models import CompanhiaAerea, Estado, InstanciaVoo


class EstadoListView(PermissionRequiredMixin, ListView):
    model = Estado
    permission_required = "voos.view_estado"
    context_object_name = "estado_list"


class CompanhiaAereaListView(PermissionRequiredMixin, ListView):
    model = CompanhiaAerea
    permission_required = "voos.view_companhiaaerea"
    permission_denied_message = "Permissão negada >:("
    context_object_name = "companhia_aerea_list"


class CompanhiaAereaCreateView(PermissionRequiredMixin, CreateView):
    model = CompanhiaAerea
    permission_required = "voos.add_companhiaaerea"
    form_class = CompanhiaAereaForm
    success_url = "/crud/companhia-aerea"


class CompanhiaAereaUpdateView(PermissionRequiredMixin, UpdateView):
    model = CompanhiaAerea
    permission_required = "voos.change_companhiaaerea"
    fields = ['nome', 'sigla']
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
    instancia_voo_list = InstanciaVoo.objects.all()
    return render(request, "voos/movimentacao.html", {"instancia_voo_list": instancia_voo_list})

def relatorio(request):
    return render(request, "voos/relatorio.html")
