# Generated by Django 5.1.7 on 2025-05-10 12:55

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pharmacie', '0011_facturepharmacie_nom_personne_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commande',
            name='fournisseur',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='pharmacie.fournisseur', verbose_name='Fournisseur'),
        ),
    ]
