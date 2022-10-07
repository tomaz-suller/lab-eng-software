from lzma import _OpenTextWritingMode
from django.db import models


# Create your models here.
class Estado(models.Model):
    nome = models.CharField(max_length=15)

    class Meta:
        db_table = 'estados'


class InstanciaVoo(models.Model):
    partida_prevista = models.DateTimeField()
    partida_real = models.DateTimeField()
    chegada_prevista = models.DateTimeField()
    chegada_real = models.DateTimeField()
    estado_atual = models.ForeignKey(Estado)
    voo = models.ForeignKey(Voo)

    class Meta:
        db_table = 'instancias_voos'


class CompanhiaAerea(models.Model):
    nome = models.CharField(max_length=100)
    sigla = models.CharField(max_length=5)

    class Meta:
        db_table = 'companhias_aereas'


class Voo(models.Model):
    codigo = models.CharField(max_length=6, primary_key=True)
    origem = models.CharField(max_length=100)
    destino = models.CharField(max_length=100)
    companhia_aerea = models.ForeignKey(CompanhiaAerea)
    class Meta:
        db_table = 'voos'
