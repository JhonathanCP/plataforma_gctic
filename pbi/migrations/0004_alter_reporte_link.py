# Generated by Django 4.2.4 on 2023-12-21 20:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pbi', '0003_reporte'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reporte',
            name='link',
            field=models.URLField(blank=True, max_length=400, null=True),
        ),
    ]