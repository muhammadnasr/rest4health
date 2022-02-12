from datetime import datetime
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User, Group
from rest_framework import viewsets,generics
from rest_framework import permissions
from restapp.serializers import UserSerializer
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from restapp.models import Table,Reservation
from restapp.serializers import TableSerializer,ReservationSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from psycopg2.extras import DateTimeRange
from rest_framework import filters as restfilters
from django_filters import rest_framework as filters
from django.db.models import Q


def index(request):
    return HttpResponse("Welcome to Rest4Health,  Your healthy restaurant!")

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class TableList(generics.ListCreateAPIView):
    queryset = Table.objects.all()
    serializer_class = TableSerializer


class TableDetail(generics.RetrieveDestroyAPIView):
    queryset = Table.objects.all()
    serializer_class = TableSerializer



