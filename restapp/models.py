from django.db import models
from django.contrib.postgres.constraints import ExclusionConstraint
from django.contrib.postgres.fields import DateTimeRangeField, RangeOperators,IntegerRangeField
from django.contrib.postgres.validators import MinValueValidator, MaxValueValidator
from psycopg2.extras import NumericRange

# Create your models here.

MIN_SEATS_COUNT = 1
MAX_SEATS_COUNT = 12

    
class Table(models.Model):
    number = models.IntegerField(default=0,primary_key=True)
    seats_count = models.IntegerField(validators=[MinValueValidator(MIN_SEATS_COUNT),
                                       MaxValueValidator(MAX_SEATS_COUNT)])

class Reservation(models.Model):
    table = models.ForeignKey('Table', on_delete=models.CASCADE)
    timespan = DateTimeRangeField()

    class Meta:
        constraints = [
            ExclusionConstraint(
                name='exclude_overlapping_reservations',
                expressions=[
                    ('timespan', RangeOperators.OVERLAPS),
                    ('table', RangeOperators.EQUAL),
                ]
            ),
        ]