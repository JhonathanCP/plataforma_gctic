# Generated by Django 5.0 on 2023-12-27 15:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pbi', '0005_permisoreporte_permisogrupo'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='cambio_primera_contrasena',
            field=models.BooleanField(default=False),
        ),
    ]
