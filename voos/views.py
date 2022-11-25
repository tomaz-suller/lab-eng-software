import datetime
from typing import Any, Dict

from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db.models import Avg, Count
from django.shortcuts import redirect, render
from django.utils import timezone
from django.views.generic import ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from .forms import VooUpdateForm, InstanciaVooUpdateForm, VooCreateForm, InstanciaVooCreateForm
from .models import CompanhiaAerea, Estado, InstanciaVoo, Movimentacao, Voo


class BaseView:
    context_object_name = "object_list"

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["model_name"] = self.model._meta.verbose_name
        context["model_fields"] = self.model._meta.fields
        context["model_endpoint"] = context["model_name"].replace(" ", "-")
        return context


class BaseCreateView(BaseView, CreateView):
    template_name = "voos/form.html"


class BaseListView(BaseView, ListView):
    template_name = "voos/list.html"


class BaseUpdateView(BaseView, UpdateView):
    template_name = "voos/form.html"


class BaseDeleteView(BaseView, DeleteView):
    template_name = "voos/confirm_delete.html"


class CompanhiaAereaListView(PermissionRequiredMixin, BaseListView):
    model = CompanhiaAerea
    permission_required = "voos.view_companhiaaerea"


class CompanhiaAereaCreateView(PermissionRequiredMixin, BaseCreateView):
    model = CompanhiaAerea
    permission_required = "voos.add_companhiaaerea"
    fields = ["nome", "sigla"]
    success_url = "/crud/companhia-aerea"


class CompanhiaAereaUpdateView(PermissionRequiredMixin, BaseUpdateView):
    model = CompanhiaAerea
    permission_required = "voos.change_companhiaaerea"
    fields = ["nome", "sigla"]
    success_url = "/crud/companhia-aerea"


class CompanhiaAereaDeleteView(PermissionRequiredMixin, BaseDeleteView):
    model = CompanhiaAerea
    permission_required = "voos.delete_companhiaaerea"
    success_url = "/crud/companhia-aerea"


class VooListView(PermissionRequiredMixin, BaseListView):
    model = Voo
    permission_required = "voos.view_voo"


class VooCreateView(PermissionRequiredMixin, BaseCreateView):
    model = Voo
    permission_required = "voos.add_voo"
    form_class = VooCreateForm
    success_url = "/crud/voo"


class VooUpdateView(PermissionRequiredMixin, BaseUpdateView):
    model = Voo
    permission_required = "voos.change_voo"
    form_class = VooUpdateForm
    success_url = "/crud/voo"


class VooDeleteView(PermissionRequiredMixin, BaseDeleteView):
    model = Voo
    permission_required = "voos.delete_voo"
    success_url = "/crud/voo"


class InstanciaVooListView(PermissionRequiredMixin, BaseListView):
    model = InstanciaVoo
    permission_required = "voos.view_instanciavoo"


class InstanciaVooCreateView(PermissionRequiredMixin, BaseCreateView):
    model = InstanciaVoo
    permission_required = "voos.add_instanciavoo"
    form_class = InstanciaVooCreateForm
    success_url = "/crud/instancia-voo"


class InstanciaVooUpdateView(PermissionRequiredMixin, BaseUpdateView):
    model = InstanciaVoo
    permission_required = "voos.change_instanciavoo"
    form_class = InstanciaVooUpdateForm
    success_url = "/crud/instancia-voo"


class InstanciaVooDeleteView(PermissionRequiredMixin, BaseDeleteView):
    model = InstanciaVoo
    permission_required = "voos.delete_instanciavoo"
    success_url = "/crud/instancia-voo"


def index(request):
    partidas = InstanciaVoo.objects.filter(voo__origem="GRU")
    chegadas = InstanciaVoo.objects.filter(voo__destino="GRU")
    context = {
        "base_pages": ["crud", "movimentacao", "relatorio"],
        "partidas": partidas,
        "chegadas": chegadas,
    }
    return render(request, "voos/index.html", context)


def lockout(request, credentials, *args, **kwargs):
    return render(request, "voos/lockout.html")


def crud(request):
    return render(request, "voos/crud.html")


def movimentacao(request):
    instancia_voo_list = InstanciaVoo.objects.all()
    return render(
        request, "voos/movimentacao.html", {"instancia_voo_list": instancia_voo_list}
    )


def relatorio(request):
    return render(request, "voos/relatorio.html")


def relatorio_partidas_chegadas(request):

    if request.POST:
        data_inicio_raw = request.POST.get("inputDataInicio")
        data_fim_raw = request.POST.get("inputDataFim")

        if (not data_inicio_raw) or (not data_fim_raw):
            return render(request, "voos/aviso_data_invalida.html")

        data_inicio = datetime.datetime.strptime(data_inicio_raw, "%Y-%m-%d").date()
        data_fim = datetime.datetime.strptime(data_fim_raw, "%Y-%m-%d").date()

        if data_fim < data_inicio:
            return render(request, "voos/aviso_data_invalida.html")

        str_data_inicio = data_inicio.strftime("%d/%m/%Y")
        str_data_fim = data_fim.strftime("%d/%m/%Y")

        partidas = (
            InstanciaVoo.objects.filter(
                partida_real__gte=data_inicio, partida_real__lte=data_fim
            )
            .values("voo__companhia_aerea__nome")
            .annotate(total=Count("voo__companhia_aerea__nome"))
            .order_by("total")
        )

        chegadas = (
            InstanciaVoo.objects.filter(
                chegada_real__gte=data_inicio, chegada_real__lte=data_fim
            )
            .values("voo__companhia_aerea__nome")
            .annotate(total=Count("voo__companhia_aerea__nome"))
            .order_by("total")
        )

        return render(
            request,
            "voos/relatorio_partidas_chegadas.html",
            {
                "partidas": partidas,
                "chegadas": chegadas,
                "str_data_inicio": str_data_inicio,
                "str_data_fim": str_data_fim,
            },
        )


def relatorio_movimentacoes(request):

    if request.POST:
        data_inicio_raw = request.POST.get("inputDataInicio")
        data_fim_raw = request.POST.get("inputDataFim")

        if (not data_inicio_raw) or (not data_fim_raw):
            return render(request, "voos/aviso_data_invalida.html")

        data_inicio = datetime.datetime.strptime(data_inicio_raw, "%Y-%m-%d").date()
        data_fim = datetime.datetime.strptime(data_fim_raw, "%Y-%m-%d").date()

        if data_fim < data_inicio:
            return render(request, "voos/aviso_data_invalida.html")

        str_data_inicio = data_inicio.strftime("%d/%m/%Y")
        str_data_fim = data_fim.strftime("%d/%m/%Y")

        movimentacoes = (
            Movimentacao.objects.filter(
                data_movimentacao__gte=data_inicio, data_movimentacao__lte=data_fim
            )
            .values("estado_anterior__nome", "estado_posterior__nome")
            .annotate(
                cont=Count("estado_anterior__nome"),
                media_tempo=Avg("tempo_movimentacao"),
            )
            .order_by("cont")
        )

        return render(
            request,
            "voos/relatorio_movimentacoes.html",
            {
                "movimentacoes": movimentacoes,
                "str_data_inicio": str_data_inicio,
                "str_data_fim": str_data_fim,
            },
        )


def movimentacao_detail(request, pk):
    state_permission_dict = {
        'Parado na origem': ['Parado na origem','Embarcando', 'Cancelado'],
        'Embarcando': ['Embarcando','Programado'],
        'Programado': ['Programado','Taxiando'],
        'Taxiando': ['Taxiando','Pronto'],
        'Pronto': ['Pronto', 'Autorizado'],
        'Autorizado': ['Autorizado','Em voo'],
        'Em voo': ['Em voo','Aterissado no destino'],
        'Cancelado': ['Cancelado'],
        'Aterissado no destino': ['Aterissado no destino']
    }

    instancia_voo = InstanciaVoo.objects.get(id=pk)
    estado_atual = instancia_voo.estado_atual.nome
    estados = Estado.objects.filter(nome__in=state_permission_dict[estado_atual])

    return render(
        request,
        "voos/movimentacao_detail.html",
        {"instancia_voo": instancia_voo, "estados": estados},
    )


def movimentacao_confirmado(request):
    id_instancia_voo = int(request.POST.get("identificador"))
    instancia_voo = InstanciaVoo.objects.get(id=id_instancia_voo)
    novo_estado_str = request.POST.get("estado")
    novo_estado = Estado.objects.get(nome=novo_estado_str)
    estado_anterior_str = request.POST.get("estado_anterior")
    estado_anterior = Estado.objects.get(nome=estado_anterior_str)

    if estado_anterior_str == novo_estado_str:
        return redirect('/movimentacao/')

    # Atualiza voo
    instancia_voo.estado_atual = novo_estado
    if novo_estado_str == 'Aterissado no destino':
        instancia_voo.chegada_real = timezone.now()
    elif novo_estado_str == 'Em voo':
        instancia_voo.partida_real = timezone.now()
    instancia_voo.save()

    # Cria novo objeto movimentacao
    lista_movs = Movimentacao.objects.filter(
        instancia_voo__id=instancia_voo.id
    ).order_by("-data_movimentacao")

    if(len(lista_movs) > 0):
        timedelta = timezone.now() - lista_movs[0].data_movimentacao
    else:
        timedelta = None
    Movimentacao.objects.create(
        data_movimentacao=timezone.now(),
        tempo_movimentacao=timedelta,
        instancia_voo=instancia_voo,
        estado_anterior=estado_anterior,
        estado_posterior=novo_estado,
    )

    return redirect("/movimentacao/")
