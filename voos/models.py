from django.db import models


class Estado(models.Model):
    nome = models.CharField(max_length=15)

    class Meta:
        db_table = "estados"


class CompanhiaAerea(models.Model):
    nome = models.CharField(max_length=100)
    sigla = models.CharField(max_length=5)

    class Meta:
        db_table = "companhias_aereas"


class Voo(models.Model):
    codigo = models.CharField(max_length=6, primary_key=True)
    origem = models.CharField(max_length=100)
    destino = models.CharField(max_length=100)
    companhia_aerea = models.ForeignKey(
        CompanhiaAerea, null=True, on_delete=models.SET_NULL
    )

    class Meta:
        db_table = "voos"


class InstanciaVoo(models.Model):
    partida_prevista = models.DateTimeField()
    partida_real = models.DateTimeField(null=True)
    chegada_prevista = models.DateTimeField()
    chegada_real = models.DateTimeField(null=True)
    estado_atual = models.ForeignKey(Estado, on_delete=models.PROTECT)
    voo = models.ForeignKey(Voo, null=True, on_delete=models.SET_NULL)

    class Meta:
        db_table = "instancias_voos"


class Movimentacao(models.Model):
    data_movimentacao = models.DateTimeField()
    tempo_movimentacao = models.DurationField(null=True)
    instancia_voo = models.ForeignKey(InstanciaVoo, on_delete=models.CASCADE)
    # related_name of '+' does not allow accessing Movimentacao from Estado
    # See https://docs.djangoproject.com/en/4.1/ref/models/fields/#django.db.models.ForeignKey.related_name  # noqa: E501
    estado_anterior = models.ForeignKey(
        Estado, on_delete=models.PROTECT, related_name="+"
    )
    estado_posterior = models.ForeignKey(
        Estado, on_delete=models.PROTECT, related_name="+"
    )

    class Meta:
        db_table = "movimentacoes"
