# Generated by Django 4.1.2 on 2022-11-06 21:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("voos", "0003_alter_companhiaaerea_nome_alter_companhiaaerea_sigla_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="instanciavoo",
            name="estado_atual",
            field=models.ForeignKey(
                blank=True,
                default=1,
                on_delete=django.db.models.deletion.PROTECT,
                to="voos.estado",
                verbose_name="estado atual",
            ),
        ),
    ]
