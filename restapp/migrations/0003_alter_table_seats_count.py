# Generated by Django 4.0.2 on 2022-02-05 18:54

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restapp', '0002_reservation_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='table',
            name='seats_count',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(12)]),
        ),
    ]