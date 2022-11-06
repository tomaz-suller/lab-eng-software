from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import render
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView
from django.db.models import Count, Avg

from .forms import CompanhiaAereaForm
from .models import CompanhiaAerea, Estado, InstanciaVoo, Movimentacao

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


class CompanhiaAereaUpdateView(PermissionRequiredMixin, UpdateView):
    model = CompanhiaAerea
    permission_required = "voos.change_companhiaaerea"
    fields = ['nome', 'sigla']
    success_url = '/crud/companhia-aerea'

class InstanciaVooUpdateView(PermissionRequiredMixin, UpdateView):
    model = InstanciaVoo
    permission_required = "voos.change_instancia_voo"
    fields = ['estado']
    success_url = '/movimentacao'

def index(request):
    partidas = InstanciaVoo.objects.filter(voo__origem="São Paulo")
    chegadas = InstanciaVoo.objects.filter(voo__destino="São Paulo")
    context = {
        "base_pages": ["crud", "movimentacao", "relatorio"],
        "partidas": partidas,
        "chegadas": chegadas
    }
    return render(request, "voos/index.html", context)

def crud(request):
    return render(request, "voos/crud.html")

def movimentacao(request):
    instancia_voo_list = InstanciaVoo.objects.all()
    return render(request, "voos/movimentacao.html", {"instancia_voo_list": instancia_voo_list})

def relatorio(request):
    return render(request, "voos/relatorio.html")

def relatorio_partidas_chegadas(request):

    if request.POST:
        data_inicio_raw = request.POST.get('inputDataInicio')
        data_fim_raw = request.POST.get('inputDataFim')

        if (not data_inicio_raw) or (not data_fim_raw):
            return render(request, 'voos/aviso_data_invalida.html')

        data_inicio = datetime.datetime.strptime(data_inicio_raw, '%Y-%m-%d').date()
        data_fim = datetime.datetime.strptime(data_fim_raw, '%Y-%m-%d').date()

        if data_fim<data_inicio:
            return render(request, 'voos/aviso_data_invalida.html')

        str_data_inicio = data_inicio.strftime('%d/%m/%Y')
        str_data_fim = data_fim.strftime('%d/%m/%Y')

        partidas = InstanciaVoo.objects.filter(
            partida_real__gte=data_inicio, partida_real__lte=data_fim
        ).values('voo__companhia_aerea__nome').annotate(total=Count('voo__companhia_aerea__nome')).order_by('total')

        chegadas = InstanciaVoo.objects.filter(
            chegada_real__gte=data_inicio, chegada_real__lte=data_fim
        ).values('voo__companhia_aerea__nome').annotate(total=Count('voo__companhia_aerea__nome')).order_by('total')
        
        return render(request, 'voos/relatorio_partidas_chegadas.html', {
            'partidas': partidas,
            'chegadas': chegadas,
            'str_data_inicio': str_data_inicio,
            'str_data_fim': str_data_fim
        })

def relatorio_movimentacoes(request):

    if request.POST:
        data_inicio_raw = request.POST.get('inputDataInicio')
        data_fim_raw = request.POST.get('inputDataFim')

        if (not data_inicio_raw) or (not data_fim_raw):
            return render(request, 'voos/aviso_data_invalida.html')

        data_inicio = datetime.datetime.strptime(data_inicio_raw, '%Y-%m-%d').date()
        data_fim = datetime.datetime.strptime(data_fim_raw, '%Y-%m-%d').date()

        if data_fim<data_inicio:
            return render(request, 'voos/aviso_data_invalida.html')
            
        str_data_inicio = data_inicio.strftime('%d/%m/%Y')
        str_data_fim = data_fim.strftime('%d/%m/%Y')

        movimentacoes = Movimentacao.objects.filter(
            data_movimentacao__gte=data_inicio, data_movimentacao__lte=data_fim
        ).values('estado_anterior__nome', 'estado_posterior__nome').annotate(cont=Count('estado_anterior__nome'), media_tempo=Avg('tempo_movimentacao')).order_by('cont')
        
        return render(request, 'voos/relatorio_movimentacoes.html', {
            'movimentacoes': movimentacoes,
            'str_data_inicio': str_data_inicio,
            'str_data_fim': str_data_fim
        })
