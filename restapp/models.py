from time import time
from django.utils import timezone
from django.db import models
from django.contrib.postgres.constraints import ExclusionConstraint
from django.contrib.postgres.fields import DateTimeRangeField, RangeOperators,IntegerRangeField
from django.contrib.postgres.validators import MinValueValidator, MaxValueValidator
from psycopg2.extras import NumericRange
from django.contrib.postgres.indexes import GistIndex

# Create your models here.
    
class Table(models.Model):
    MIN_SEATS_COUNT = 1
    MAX_SEATS_COUNT = 12
    
    number = models.IntegerField(default=0,primary_key=True)
    seats_count = models.IntegerField(validators=[MinValueValidator(MIN_SEATS_COUNT),
                                       MaxValueValidator(MAX_SEATS_COUNT)])

class Reservation(models.Model):
    @staticmethod
    def start_of_day():
        return timezone.now().replace(hour=12,minute=0,second=0,microsecond=0)

    @staticmethod
    def end_of_day():
        return timezone.now().replace(hour=23,minute=59,second=0,microsecond=0)

    table = models.ForeignKey(Table, on_delete=models.RESTRICT)
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
        indexes = [
            (GistIndex(fields=['timespan'])),
        ]
