import imp
from django.contrib.auth.models import User
from rest_framework import serializers
from restapp.models import Table

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class TableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Table
        fields = ['number', 'seats_count']

