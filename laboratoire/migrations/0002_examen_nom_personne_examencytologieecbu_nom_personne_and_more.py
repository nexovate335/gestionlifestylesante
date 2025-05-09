# Generated by Django 5.1.7 on 2025-05-09 22:04

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('laboratoire', '0001_initial'),
        ('patients', '0011_alter_patient_age'),
    ]

    operations = [
        migrations.AddField(
            model_name='examen',
            name='nom_personne',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Nom complet de la personne concernée'),
        ),
        migrations.AddField(
            model_name='examencytologieecbu',
            name='nom_personne',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Nom complet de la personne concernée'),
        ),
        migrations.AddField(
            model_name='examencytologiepv',
            name='nom_personne',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Nom complet de la personne concernée'),
        ),
        migrations.AddField(
            model_name='resultat',
            name='nom_personne',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Nom complet de la personne concernée'),
        ),
        migrations.AlterField(
            model_name='examen',
            name='patient',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='patients.patient', verbose_name='Patient'),
        ),
        migrations.AlterField(
            model_name='examencytologieecbu',
            name='patient',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='patients.patient', verbose_name='Patient'),
        ),
        migrations.AlterField(
            model_name='examencytologiepv',
            name='patient',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='patients.patient', verbose_name='Patient'),
        ),
        migrations.AlterField(
            model_name='resultat',
            name='patient',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='patients.patient', verbose_name='Patient'),
        ),
    ]
