# Generated by Django 5.0.3 on 2024-04-27 20:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Proyectos', '0004_alter_categoria_imgenobjeto'),
    ]

    operations = [
        migrations.AlterField(
            model_name='categoria',
            name='imgenobjeto',
            field=models.ImageField(max_length=1000, upload_to=None, verbose_name=''),
        ),
    ]
