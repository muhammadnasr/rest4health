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
    def validate(self, data):
        if data['timespan'].lower.time() < Reservation.start_of_day().time():
            raise serializers.ValidationError("cannot reserver before restaurant start time")
        if data['timespan'].upper.time() > Reservation.end_of_day().time():
            raise serializers.ValidationError("cannot reserver after restaurant finish time")
        return data

    class Meta:
        model = Reservation
        fields = ['id','table','timespan']