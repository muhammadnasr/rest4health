# Generated by Django 4.0.2 on 2022-02-12 17:25

import django.contrib.postgres.indexes
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('restapp', '0001_initial'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='reservation',
            index=django.contrib.postgres.indexes.GistIndex(fields=['timespan'], name='restapp_res_timespa_b1f401_gist'),
        ),
    ]
    