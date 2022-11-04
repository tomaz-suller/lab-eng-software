from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import render
from django.views.generic import ListView
from django.views.generic.edit import CreateView
from django.db.models import Count

from .forms import CompanhiaAereaForm
from .models import CompanhiaAerea, Estado, InstanciaVoo

import datetime


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

def relatorio_partidas_chegadas(request):

    if request.POST:
        data_inicio = datetime.datetime.strptime(request.POST.get('inputDataInicio'), '%Y-%m-%d').date()
        data_fim = datetime.datetime.strptime(request.POST.get('inputDataFim'), '%Y-%m-%d').date()

        partidas = InstanciaVoo.objects.filter(
            partida_real__gte=data_inicio, partida_real__lte=data_fim
        ).values('voo__companhia_aerea__nome').annotate(total=Count('voo__companhia_aerea__nome')).order_by('total')

        chegadas = InstanciaVoo.objects.filter(
            chegada_real__gte=data_inicio, chegada_real__lte=data_fim
        ).values('voo__companhia_aerea__nome').annotate(total=Count('voo__companhia_aerea__nome')).order_by('total')
        
        return render(request, 'voos/relatorio_partidas_chegadas.html', {'partidas': partidas, 'chegadas': chegadas})
