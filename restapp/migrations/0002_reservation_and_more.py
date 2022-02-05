# Generated by Django 4.0.2 on 2022-02-05 18:11

import django.contrib.postgres.constraints
import django.contrib.postgres.fields.ranges
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('restapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timespan', django.contrib.postgres.fields.ranges.DateTimeRangeField()),
                ('table', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='restapp.table')),
            ],
        ),
        migrations.AddConstraint(
            model_name='reservation',
            constraint=django.contrib.postgres.constraints.ExclusionConstraint(expressions=[('timespan', '&&'), ('table', '=')], name='exclude_overlapping_reservations'),
        ),
    ]
