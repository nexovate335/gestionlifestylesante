# Generated by Django 5.1.7 on 2025-04-13 13:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('caisse', '0015_rapportjournaliercaisse'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rapportjournaliercaisse',
            name='date',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Date du rapport'),
        ),
    ]
