from django.test import TestCase

# Create your tests here.
from voos.models import Movimentacao, Estado
class MovimentacaoModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Movimentacao.objects.create(titulo='Os Irmãos Karamazov',isbn='000000')
    def test_criacao_id(self):
        movimentacao_1 = Movimentacao.objects.get(titulo='Os Irmãos Karamazov')
        self.assertEqual(movimentacao_1.id, 1)
    def test_update_titulo(self):
        movimentacao_1 = Movimentacao.objects.get(titulo='Os Irmãos Karamazov')
        movimentacao_1.titulo = "Outro nome"
        movimentacao_1.save()
        self.assertEqual(movimentacao_1.titulo, "Outro nome")
#incompleto
class EstadoModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Estado.objects.create(nome="Embarcando")

    def test_criacao_id(self):
        estado_1 = Estado.objects.get(nome="Embarcando")
        self.assertEqual(estado_1.id, 1)

    def test_update_estado(self):
        estado_1 = Estado.objects.get(titulo='Embarcando')
        estado_1.titulo = "Taxiando"
        estado_1.save()
        self.assertEqual(estado_1.titulo, "Taxiando")