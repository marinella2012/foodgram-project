# Generated by Django 3.2.3 on 2021-06-27 19:01

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='cooking_time',
            field=models.PositiveSmallIntegerField(default=0, validators=[django.core.validators.MinValueValidator(1)], verbose_name='Время приготовления'),
        ),
    ]