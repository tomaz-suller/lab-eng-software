# Generated by Django 4.1.2 on 2022-11-25 18:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('voos', '0006_alter_voo_codigo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='estado',
            name='nome',
            field=models.CharField(max_length=30),
        ),
    ]