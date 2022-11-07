from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Dict, Iterable, Union
from unittest import expectedFailure

from django.template.response import TemplateResponse
from django.test import TestCase

from voos.models import CompanhiaAerea, Estado, InstanciaVoo, Movimentacao, Voo


class MonitoramentoAvioesTestFixture(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        departure_datetime = datetime(2022, 1, 1, 1, 0, tzinfo=timezone.utc)
        cls.estado_autorizado = Estado.objects.create(nome="Autorizado")
        cls.estado_voando = Estado.objects.create(nome="Em voo")
        cls.companhia = CompanhiaAerea.objects.create(
            nome="American Airlines", sigla="AA"
        )
        cls.voo = Voo.objects.create(
            codigo="AA1234",
            origem="GRU",
            destino="SDU",
            companhia_aerea=cls.companhia,
        )
        cls.instancia_voo = InstanciaVoo.objects.create(
            partida_prevista=departure_datetime,
            partida_real=None,
            chegada_prevista=departure_datetime + timedelta(hours=10),
            chegada_real=None,
            estado_atual=cls.estado_voando,
            voo=cls.voo,
        )
        cls.movimentacao = Movimentacao.objects.create(
            data_movimentacao=departure_datetime,
            tempo_movimentacao=None,
            instancia_voo=cls.instancia_voo,
            estado_anterior=cls.estado_autorizado,
            estado_posterior=cls.estado_voando,
        )
        return super().setUpTestData()


class MovimentacaoTest(MonitoramentoAvioesTestFixture):
    def test_criacao_id(self):
        self.assertEqual(self.movimentacao.id, 1)

    def test_update_estado_anterior(self):
        aterrissado = Estado.objects.create(nome="Aterrissado")
        self.movimentacao.estado_anterior = aterrissado
        self.movimentacao.save()
        movimentacao_1 = Movimentacao.objects.get(id=1)
        self.assertEqual(movimentacao_1.estado_anterior, aterrissado)

    def test_update_estado_posterior(self):
        embarcado = Estado.objects.create(nome="Embarcado")
        self.movimentacao.estado_posterior = embarcado
        self.movimentacao.save()
        movimentacao_1 = Movimentacao.objects.get(id=1)
        self.assertEqual(movimentacao_1.estado_posterior, embarcado)

    def test_delete(self):
        movimentacao = Movimentacao.objects.get(id=1)
        movimentacao.delete()
        self.assertEqual(len(list(Movimentacao.objects.all())), 0)


class EstadoTest(MonitoramentoAvioesTestFixture):
    def test_criacao_id(self):
        estado_1 = Estado.objects.get(nome="Autorizado")
        self.assertEqual(estado_1.id, 1)

    def test_update_estado(self):
        estado_1 = Estado.objects.get(nome="Autorizado")
        estado_1.nome = "Em voo"
        estado_1.save()
        self.assertEqual(estado_1.nome, "Em voo")


class CompanhiaAereaTest(MonitoramentoAvioesTestFixture):
    def test_criacao_id(self):
        companhia_1 = CompanhiaAerea.objects.get(nome="American Airlines")
        self.assertEqual(companhia_1.id, 1)

    def test_update_nome(self):
        companhia_1 = CompanhiaAerea.objects.get(nome="American Airlines")
        companhia_1.nome = "Companhia B"
        companhia_1.save()
        self.assertEqual(companhia_1.nome, "Companhia B")

    def test_delete(self):
        companhia_1 = CompanhiaAerea.objects.get(sigla="AA")
        companhia_1.delete()
        self.assertEqual(len(list(CompanhiaAerea.objects.all())), 0)


class VooTest(MonitoramentoAvioesTestFixture):
    def test_criacao_id(self):
        voo_1 = Voo.objects.get(codigo="AA1234")
        self.assertEqual(voo_1.codigo, "AA1234")

    def test_update_destino(self):
        voo_1 = Voo.objects.get(codigo="AA1234")
        voo_1.destino = "LHR"
        voo_1.save()
        self.assertEqual(voo_1.destino, "LHR")

    def test_delete(self):
        voo_1 = Voo.objects.get(codigo="AA1234")
        voo_1.delete()
        self.assertEqual(len(list(Voo.objects.all())), 0)


class InstanciaVooTest(MonitoramentoAvioesTestFixture):
    def test_criacao_id(self):
        self.assertEqual(self.instancia_voo.id, 1)

    def test_update_estado_atual(self):
        aterrissado = Estado.objects.create(nome="Aterrissado")
        self.instancia_voo.estado_atual = aterrissado
        self.instancia_voo.save()
        instancia_voo = InstanciaVoo.objects.get(id=1)
        self.assertEqual(instancia_voo.estado_atual, aterrissado)

    def test_delete(self):
        self.instancia_voo.delete()
        self.assertFalse(InstanciaVoo.objects.exists())

    def test_delete_cascades_to_movimentacao(self):
        movimentacao_set = self.instancia_voo.movimentacao_set.all()
        self.instancia_voo.delete()
        for movimentacao in movimentacao_set:
            self.assertFalse(Movimentacao.objects.contains(movimentacao))


@dataclass
class CrudUrls:
    base: str

    @staticmethod
    def join_url(*args: str, absolute: bool = False) -> str:
        url = "/".join(args)
        if absolute:
            url = "/" + url
        return url

    def __post_init__(self):
        self.create = self.join_url(self.base, "criar")
        self.read = self.base
        self.update = self.join_url(self.base, "alterar", "{pk}")
        self.delete = self.join_url(self.base, "apagar", "{pk}")


class ViewTestFixture:
    url: Union[str, CrudUrls]
    template: str
    allowed_credentials: Iterable[Dict[str, str]]
    forbidden_credentials: Iterable[Dict[str, str]]
    read_content: Iterable[str] = None
    create_content: Dict[str, str] = None
    update_content: Dict[str, str] = None
    delete_pk: str = None
    fixtures = ["db.json"]

    def setUp(self):
        self.client.login(username="admin", password="admin")
        self.url = CrudUrls(self.url)

    def _create(self, payload: Dict[str, str]):
        return self.client.post(self.url.create, payload)

    def _read(self):
        return self.client.get(self.url.read)

    def _update(self, pk: str, payload: Dict[str, str]):
        return self.client.post(self.url.update.format(pk=pk), payload)

    def _delete(self, pk: str):
        return self.client.post(self.url.delete.format(pk=pk))

    def _test_in_rendered_page(self, response: TemplateResponse, *content: str):
        response_content: bytes = response.content
        for content_string in content:
            with self.subTest(content=content_string):
                self.assertTrue(content_string.encode("utf8") in response_content)

    def test_url_accessible(self):
        response = self._read()
        self.assertEquals(response.status_code, 200)
        return response

    def test_permissions(self):
        expected_status_codes = [200] * len(self.allowed_credentials) + [403] * len(
            self.forbidden_credentials
        )
        for credentials, expected_status_code in zip(
            self.allowed_credentials + self.forbidden_credentials, expected_status_codes
        ):
            with self.subTest(username=credentials["username"]):
                self.client.login(**credentials)
                response = self._read()
                self.assertEquals(response.status_code, expected_status_code)

    def test_create(self):
        if self.create_content is None:
            self.skipTest("No content to create")
        else:
            response = self._create(self.create_content)
            self.assertEquals(response.status_code, 302)  # 302: Redirect
            self.assertEquals(response.url, self.url.read)

            response = self._read()
            self._test_in_rendered_page(
                response,
                *self.create_content.values(),
            )

    def test_read(self):
        if self.read_content is None:
            self.skipTest("No page content")
        else:
            response = self._read()
            self._test_in_rendered_page(response, *self.read_content)

    def test_update(self):
        if self.update_content is None:
            self.skipTest("No content to update")
        else:
            pk = self.update_content.pop("pk", "1")
            response = self._update(pk, self.update_content)
            self.assertEquals(response.status_code, 302)  # 302: Redirect
            self.assertEquals(response.url, self.url.read)

            response = self._read()
            self._test_in_rendered_page(
                response,
                *self.update_content.values(),
            )

    def test_delete(self):
        pk = self.delete_pk or "1"
        response = self._delete(pk)
        self.assertEquals(response.status_code, 302)  # 302: Redirect
        self.assertEquals(response.url, self.url.read)

    @expectedFailure
    def test_delete_removes_content(self):
        self.test_delete()
        response = self._read()
        self._test_in_rendered_page(response, *self.read_content)


class CompanhiaAereaViewTest(ViewTestFixture, MonitoramentoAvioesTestFixture):
    url = "/crud/companhia-aerea"
    allowed_credentials = [
        {"username": "admin", "password": "admin"},
    ]
    forbidden_credentials = [
        {"username": "piloto", "password": "senha-do-piloto"},
    ]
    read_content = (
        "Companhia Aerea",
        "Nome",
        "Sigla",
        "American Airlines",
        "AA",
    )
    create_content = {
        "nome": "JetBlue",
        "sigla": "JBU",
    }
    update_content = {
        "nome": "JetBlue",
        "sigla": "JBL",
    }


class InstanciaVooViewTest(ViewTestFixture, MonitoramentoAvioesTestFixture):
    url = "/crud/instancia-voo"
    allowed_credentials = [
        {"username": "admin", "password": "admin"},
    ]
    read_content = (
        "Instancia Voo",
        "Hora De Partida Prevista",
        "Hora De Partida",
        "Hora De Chegada Prevista",
        "Hora De Chegada",
        "Estado Atual",
        "Rota",
        "1/1/2022 01:00",
        "None",
        "1/1/2022 11:00",
        "None",
        "Estado Em voo",
        "Rota AA1234",
    )
    create_content = {
        "partida_prevista": "1/1/2022 02:00",
        "partida_real": "",
        "chegada_prevista": "1/1/2022 12:00",
        "chegada_real": "",
        "voo": "AA1234",
    }
    update_content = {
        "partida_prevista": "1/1/2022 02:00",
        "partida_real": "1/1/2022 01:00",
        "chegada_prevista": "1/1/2022 12:00",
        "chegada_real": "1/1/2022 11:00",
        "voo": "AA1234",
    }


class VooViewTest(ViewTestFixture, MonitoramentoAvioesTestFixture):
    url = "/crud/voo"
    allowed_credentials = [
        {"username": "admin", "password": "admin"},
    ]
    forbidden_credentials = [
        {"username": "piloto", "password": "senha-do-piloto"},
    ]
    read_content = (
        "Voo",
        "Código",
        "Origem",
        "Destino",
        "Companhia Aérea",
        "AA1234",
        "GRU",
        "SDU",
        "Companhia aérea American Airlines",
    )
    create_content = {
        "codigo": "AA4321",
        "origem": "USA",
        "destino": "BRA",
        "companhia_aerea": "1",
    }
    update_content = {
        "pk": "AA1234",
        "codigo": "AA4321",
        "origem": "FRA",
        "destino": "BRA",
        "companhia_aerea": "1",
    }
    delete_pk = "AA1234"


class RelatoriosTestFixture(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        departure_datetime = datetime(2022, 1, 1, 1, 0, tzinfo=timezone.utc)
        cls.estado_autorizado = Estado.objects.create(nome="Autorizado")
        cls.estado_voando = Estado.objects.create(nome="Em voo")
        cls.companhia = CompanhiaAerea.objects.create(
            nome="American Airlines", sigla="AA"
        )
        cls.voo = Voo.objects.create(
            codigo="AA1234",
            origem="GRU",
            destino="SDU",
            companhia_aerea=cls.companhia,
        )
        cls.instancia_voo = InstanciaVoo.objects.create(
            partida_prevista=departure_datetime,
            partida_real=departure_datetime,
            chegada_prevista=departure_datetime + timedelta(hours=10),
            chegada_real=departure_datetime + timedelta(hours=10),
            estado_atual=cls.estado_voando,
            voo=cls.voo,
        )
        cls.movimentacao = Movimentacao.objects.create(
            data_movimentacao=departure_datetime,
            tempo_movimentacao=None,
            instancia_voo=cls.instancia_voo,
            estado_anterior=cls.estado_autorizado,
            estado_posterior=cls.estado_voando,
        )
        return super().setUpTestData()


class RelatoriosTest(RelatoriosTestFixture):
    def test_acesso(self):
        response = self.client.get("/relatorio")
        self.assertTrue(response.status_code == 200)

    def test_relatorio_partidas_chegadas(self):
        response = self.client.post(
            "/relatorio/partidas-chegadas",
            {"inputDataInicio": "2020-01-01", "inputDataFim": "2022-12-01"},
        )
        self.assertTrue(response.status_code == 200)
        self.assertTrue(len(response.context["partidas"]) == 1)
        self.assertTrue(len(response.context["chegadas"]) == 1)

    def test_relatorio_movimentacoes(self):
        response = self.client.post(
            "/relatorio/movimentacoes",
            {"inputDataInicio": "2020-01-01", "inputDataFim": "2022-12-01"},
        )
        self.assertTrue(response.status_code == 200)
        self.assertTrue(len(response.context["movimentacoes"]) == 1)

    def test_data_invalida(self):
        response = self.client.post(
            "/relatorio/movimentacoes",
            {"inputDataInicio": "2022-01-01", "inputDataFim": "2020-12-01"},
        )
        self.assertTrue(response.status_code == 200)
        self.assertContains(response, "Período inválido")

    def test_periodo_vazio(self):
        response = self.client.post(
            "/relatorio/partidas-chegadas",
            {"inputDataInicio": "2020-01-01", "inputDataFim": "2020-01-01"},
        )
        self.assertTrue(response.status_code == 200)
        self.assertTrue(len(response.context["partidas"]) == 0)
        self.assertTrue(len(response.context["chegadas"]) == 0)


class IndexTest(RelatoriosTestFixture):
    def test_acesso(self):
        response = self.client.get("/")
        self.assertTrue(response.status_code == 200)
        self.assertTrue(len(response.context["partidas"]) == 1)
        self.assertTrue(len(response.context["chegadas"]) == 0)
