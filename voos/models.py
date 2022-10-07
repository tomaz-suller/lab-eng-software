from lzma import _OpenTextWritingMode
from django.db import models

# Create your models here.
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