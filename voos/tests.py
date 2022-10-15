from datetime import datetime, timedelta, timezone

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
