# Generated by Django 5.1.3 on 2024-11-24 20:49

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('noivos', '0002_convidados'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='presentes',
            options={'verbose_name': 'Presente', 'verbose_name_plural': 'Presentes'},
        ),
        migrations.AddField(
            model_name='presentes',
            name='reservado_por',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='noivos.convidados'),
        ),
    ]