# Generated by Django 5.1.3 on 2024-12-26 23:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('noivos', '0003_alter_presentes_options_presentes_reservado_por'),
    ]

    operations = [
        migrations.AddField(
            model_name='convidados',
            name='acompanhantes_confirmados',
            field=models.PositiveIntegerField(default=0),
        ),
    ]