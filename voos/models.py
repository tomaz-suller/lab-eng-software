from django.db import models
from django.core.validators import RegexValidator


class Estado(models.Model):
    nome = models.CharField(max_length=30)

    def __str__(self) -> str:
        return f"Estado {self.nome}"

    class Meta:
        db_table = "estados"


class CompanhiaAerea(models.Model):
    nome = models.CharField(max_length=100, verbose_name="nome")
    sigla = models.CharField(
        max_length=5, verbose_name="sigla",
        validators=[RegexValidator(r"[A-Z]{3}", "Sigla da companhia aérea deve ser composta de três caracteres maiúsculos.")]
    )

    def __str__(self) -> str:
        return f"Companhia aérea {self.nome} ({self.sigla})"

    class Meta:
        db_table = "companhias_aereas"


class Voo(models.Model):
    codigo = models.CharField(
        max_length=6, primary_key=True, verbose_name="código",
        validators=[RegexValidator(r"[A-Z]{2}[0-9]{4}", "Código de voo deve ser composto de dois caracteres maiúsculos seguidos de quatro dígitos.")]
    )
    origem = models.CharField(max_length=100, verbose_name="origem")
    destino = models.CharField(max_length=100, verbose_name="destino")
    companhia_aerea = models.ForeignKey(
        CompanhiaAerea,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name="companhia aérea",
    )

    def __str__(self) -> str:
        return f"Rota {self.codigo}"

    class Meta:
        db_table = "voos"


class InstanciaVoo(models.Model):
    partida_prevista = models.DateTimeField(verbose_name="hora de partida prevista")
    partida_real = models.DateTimeField(
        null=True, blank=True, verbose_name="hora de partida"
    )
    chegada_prevista = models.DateTimeField(verbose_name="hora de chegada prevista")
    chegada_real = models.DateTimeField(
        null=True, blank=True, verbose_name="hora de chegada"
    )
    estado_atual = models.ForeignKey(
        Estado,
        blank=True,
        null=True,
        on_delete=models.PROTECT,
        verbose_name="estado atual",
    )
    voo = models.ForeignKey(
        Voo, null=True, on_delete=models.SET_NULL, verbose_name="rota"
    )


    def save(self, *args, **kwargs):
        if not self.estado_atual:
            if self.voo.destino == "GRU":
                self.estado_atual = Estado.objects.get(nome="Em voo")
            else:
                self.estado_atual = Estado.objects.get(nome="Parado na origem")

        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"Voo {self.id} associado a {self.voo}"

    class Meta:
        db_table = "instancias_voos"


class Movimentacao(models.Model):
    data_movimentacao = models.DateTimeField(verbose_name="data")
    tempo_movimentacao = models.DurationField(
        null=True, verbose_name="intervalo entre movimentações"
    )
    instancia_voo = models.ForeignKey(
        InstanciaVoo, on_delete=models.CASCADE, verbose_name="voo"
    )
    # related_name of '+' does not allow accessing Movimentacao from Estado
    # See https://docs.djangoproject.com/en/4.1/ref/models/fields/#django.db.models.ForeignKey.related_name  # noqa: E501
    estado_anterior = models.ForeignKey(
        Estado,
        on_delete=models.PROTECT,
        related_name="+",
        verbose_name="estado anterior",
    )
    estado_posterior = models.ForeignKey(
        Estado,
        on_delete=models.PROTECT,
        related_name="+",
        verbose_name="estado posterior",
    )

    def __str__(self) -> str:
        return (
            f"Mudança de {self.estado_anterior} "
            f"para {self.estado_posterior} "
            f"associada a {self.instancia_voo}"
        )

    class Meta:
        db_table = "movimentacoes"
