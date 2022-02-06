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
from datetime import datetime
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


class TimespanFilter(filters.FilterSet):
    timespan = filters.DateFromToRangeFilter()

    class Meta:
        model = Reservation
        fields = [
            "timespan",
            "table",
        ]

class ReservationList(generics.ListCreateAPIView):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    filter_backends = [filters.DjangoFilterBackend]
    filter_class = TimespanFilter

class ReservationDetail(generics.RetrieveDestroyAPIView):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer


#not fully working
class ReservationAvailable(APIView):

    def get(self, request, seats_count, format=None):
        start_of_today = datetime.now().replace(hour=12,minute=0,second=0,microsecond=0)
        reservations = Reservation.objects.filter(table__seats_count=seats_count).filter(timespan__startswith__gte=start_of_today)
        print(reservations)
        serializer = ReservationSerializer(reservations, many=True)
        return Response(serializer.data)

class ReservationToday(generics.ListAPIView):
    start_of_today = datetime.now().replace(hour=12,minute=0,second=0,microsecond=0)
    queryset = Reservation.objects.filter(timespan__startswith__gte=start_of_today)
    serializer_class = ReservationSerializer
    filter_backends = [restfilters.OrderingFilter]
    ordering_fields = ['timespan']



