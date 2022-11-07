from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView
from django.db.models import Count, Avg
from django.utils import timezone

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
    partidas = InstanciaVoo.objects.filter(voo__origem="GRU")
    chegadas = InstanciaVoo.objects.filter(voo__destino="GRU")
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

def movimentacao_detail(request, pk):
    instancia_voo = InstanciaVoo.objects.get(id=pk)
    estados = Estado.objects.all()

    return render(request, 'voos/movimentacao_detail.html', {
        'instancia_voo':instancia_voo,
        'estados':estados
    })

def movimentacao_confirmado(request):
    id_instancia_voo = int(request.POST.get('identificador'))
    instancia_voo = InstanciaVoo.objects.get(id=id_instancia_voo)
    novo_estado_str = request.POST.get('estado')
    novo_estado = Estado.objects.get(nome=novo_estado_str)
    estado_anterior_str = request.POST.get('estado_anterior')
    estado_anterior = Estado.objects.get(nome=estado_anterior_str)

    # Atualiza voo
    instancia_voo.estado_atual = novo_estado
    instancia_voo.save()

    # Cria novo objeto movimentacao
    ultima_mov = Movimentacao.objects.filter(instancia_voo__id=instancia_voo.id).order_by('-data_movimentacao')[0]
    timedelta = timezone.now() - ultima_mov.data_movimentacao
    movimentacao = Movimentacao.objects.create(
        data_movimentacao=datetime.datetime.now(),
        tempo_movimentacao=timedelta,
        instancia_voo=instancia_voo,
        estado_anterior=estado_anterior,
        estado_posterior=novo_estado,
    )

    return redirect('/')
