# Generated by Django 4.2.4 on 2023-11-05 19:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contabilidad', '0010_cuenta_cuenta_av_alter_cuenta_subcategoria'),
    ]

    operations = [
        migrations.AddField(
            model_name='cuenta',
            name='categoria_av',
            field=models.CharField(choices=[('NNG', 'Ninguna'), ('ASV', 'Activo'), ('PSV', 'Pasivo'), ('PTR', 'Patrimonio'), ('ESR', 'Estado de Resultados')], default='NNG', max_length=5),
        ),
    ]
