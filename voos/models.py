#from lzma import _OpenTextWritingMode
from django.db import models

# Create your models here.
class Estado(models.Model):
    nome = models.CharField(max_length=15)

    class Meta:
        db_table = 'estados'

class CompanhiaAerea(models.Model):
    nome = models.CharField(max_length=100)
    sigla = models.CharField(max_length=5)

    class Meta:
        db_table = 'companhias_aereas'

class Voo(models.Model):
    codigo = models.CharField(max_length=6, primary_key=True)
    origem = models.CharField(max_length=100)
    destino = models.CharField(max_length=100)
    companhia_aerea = models.ForeignKey(CompanhiaAerea, on_delete=models.CASCADE)
    class Meta:
        db_table = 'voos'

class InstanciaVoo(models.Model):
    partida_prevista = models.DateTimeField()
    partida_real = models.DateTimeField()
    chegada_prevista = models.DateTimeField()
    chegada_real = models.DateTimeField()
    estado_atual = models.ForeignKey(Estado, on_delete=models.CASCADE)
    voo = models.ForeignKey(Voo, on_delete=models.CASCADE)
    class Meta:
        db_table = 'instancias_voos'
class Movimentacao(models.Model):
    data_movimentacao = models.DateTimeField()
    tempo_movimentacao = models.DurationField()
    instancia_voo = models.ForeignKey(InstanciaVoo, on_delete=models.CASCADE)
    estado_anterior = models.ForeignKey(Estado, on_delete=models.CASCADE, related_name='estado_anterior')
    estado_posterior = models.ForeignKey(Estado, on_delete=models.CASCADE, related_name='estado_posterior')
    class Meta:
        db_table = 'movimentacoes'