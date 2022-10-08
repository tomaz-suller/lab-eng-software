# Generated by Django 4.1.2 on 2022-10-08 17:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("voos", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="instanciavoo",
            name="chegada_real",
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name="instanciavoo",
            name="estado_atual",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT, to="voos.estado"
            ),
        ),
        migrations.AlterField(
            model_name="instanciavoo",
            name="partida_real",
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name="instanciavoo",
            name="voo",
            field=models.ForeignKey(
                null=True, on_delete=django.db.models.deletion.SET_NULL, to="voos.voo"
            ),
        ),
        migrations.AlterField(
            model_name="movimentacao",
            name="estado_anterior",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name="+",
                to="voos.estado",
            ),
        ),
        migrations.AlterField(
            model_name="movimentacao",
            name="estado_posterior",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name="+",
                to="voos.estado",
            ),
        ),
        migrations.AlterField(
            model_name="movimentacao",
            name="tempo_movimentacao",
            field=models.DurationField(null=True),
        ),
        migrations.AlterField(
            model_name="voo",
            name="companhia_aerea",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="voos.companhiaaerea",
            ),
        ),
    ]