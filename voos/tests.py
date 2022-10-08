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


class MovimentacaoModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Movimentacao.objects.create(titulo="Os Irmãos Karamazov", isbn="000000")

    def test_criacao_id(self):
        movimentacao_1 = Movimentacao.objects.get(titulo="Os Irmãos Karamazov")
        self.assertEqual(movimentacao_1.id, 1)

    def test_update_titulo(self):
        movimentacao_1 = Movimentacao.objects.get(titulo="Os Irmãos Karamazov")
        movimentacao_1.titulo = "Outro nome"
        movimentacao_1.save()
        self.assertEqual(movimentacao_1.titulo, "Outro nome")


# incompleto
class EstadoModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Estado.objects.create(nome="Embarcando")

    def test_criacao_id(self):
        estado_1 = Estado.objects.get(nome="Embarcando")
        self.assertEqual(estado_1.id, 1)

    def test_update_estado(self):
        estado_1 = Estado.objects.get(titulo="Embarcando")
        estado_1.titulo = "Taxiando"
        estado_1.save()
        self.assertEqual(estado_1.titulo, "Taxiando")


# Teste da classe CompanhiaAerea
class CompanhiaAereaTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        CompanhiaAerea.objects.create(nome="Companhia A", sigla="AAA")

    def test_criacao_id(self):
        companhia_1 = CompanhiaAerea.objects.get(nome="Companhia A")
        self.assertEqual(companhia_1.id, 1)

    def test_update_nome(self):
        companhia_1 = CompanhiaAerea.objects.get(nome="Companhia A")
        companhia_1.nome = "Companhia B"
        companhia_1.save()
        self.assertEqual(companhia_1.nome, "Companhia B")

    def test_delete(self):
        companhia_1 = CompanhiaAerea.objects.get(sigla="AAA")
        companhia_1.delete()
        self.assertEqual(len(list(CompanhiaAerea.objects.all())), 0)


# Teste da classe Voo
class VooTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        companhia_1 = CompanhiaAerea.objects.create(nome="Companhia A", sigla="AAA")
        Voo.objects.create(
            codigo="AB1234",
            origem="GRU",
            destino="SDU",
            companhia_aerea=companhia_1,
        )

    def test_criacao_id(self):
        voo_1 = Voo.objects.get(codigo="AB1234")
        self.assertEqual(voo_1.codigo, "AB1234")

    def test_update_destino(self):
        voo_1 = Voo.objects.get(codigo="AB1234")
        voo_1.destino = "LHR"
        voo_1.save()
        self.assertEqual(voo_1.destino, "LHR")

    def test_delete(self):
        voo_1 = Voo.objects.get(codigo="AB1234")
        voo_1.delete()
        self.assertEqual(len(list(Voo.objects.all())), 0)
