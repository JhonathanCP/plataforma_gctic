# Generated by Django 4.1.9 on 2023-12-29 06:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pbi', '0005_permisoreporte_permisogrupo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reporte',
            name='grupo',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reportes', to='pbi.grupo'),
        ),
    ]