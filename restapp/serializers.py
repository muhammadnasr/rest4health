import imp
from django.contrib.auth.models import User
from rest_framework import serializers
from restapp.models import Table,Reservation

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class TableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Table
        fields = ['number', 'seats_count']

class ReservationSerializer(serializers.ModelSerializer):
    #table = TableSerializer( read_only=True)

    class Meta:
        model = Reservation
        fields = ['id','table','timespan']