from django.db import models

# Create your models here.

class Table(models.Model):
    number = models.IntegerField(default=0,primary_key=True)
    seats_count = models.IntegerField()
