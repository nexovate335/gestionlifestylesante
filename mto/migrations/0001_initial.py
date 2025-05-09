# Generated by Django 5.1.7 on 2025-04-22 08:30

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('patients', '0009_patient_assistant_patient_medecin'),
    ]

    operations = [
        migrations.CreateModel(
            name='Mto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('demandeur', models.CharField(blank=True, max_length=100, null=True, verbose_name='Demandeur')),
                ('pratiqueur', models.CharField(blank=True, max_length=100, null=True, verbose_name='Pratiqueur')),
                ('montant', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Montant')),
                ('resultat', models.TextField(blank=True, null=True, verbose_name='Résultat')),
                ('commentaire', models.TextField(blank=True, max_length=1000, null=True, verbose_name='Commentaire')),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name='Date et heure de création')),
                ('deleted_at', models.DateTimeField(blank=True, null=True, verbose_name='Date de suppression')),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='patients.patient', verbose_name='Patient')),
            ],
            options={
                'verbose_name': 'Mto',
                'verbose_name_plural': 'Mto',
            },
        ),
    ]
