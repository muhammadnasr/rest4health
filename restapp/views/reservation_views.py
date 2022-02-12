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

class ReservationAvailable(APIView):

    def get(self, request, seats_count, format=None):

        available_reservations = []
        while not available_reservations and seats_count <= Table.MAX_SEATS_COUNT:
            available_reservations.extend(ReservationAvailable.find_available_reservation_for_seats_count(seats_count))
            seats_count = seats_count + 1

        serializer = ReservationSerializer(available_reservations, many=True)
        return Response(serializer.data)

 
    @staticmethod
    def find_available_reservation_for_seats_count(seats_count):
        reservations = Reservation.objects.filter(table__seats_count=seats_count).filter(timespan__startswith__gte=Reservation.start_of_day() ).order_by('timespan')
        tables = Table.objects.filter(seats_count=seats_count)

        reservations_by_table = {}
        for table in tables:
            reservations_by_table[table] = []

        for reservation in reservations:
            reservations_by_table[reservation.table].append(reservation)

        available_reservations = []
        for table in reservations_by_table:
            available_reservations.extend(ReservationAvailable.find_available_reservation_for_table(table,reservations_by_table[table]))

        return available_reservations

    @staticmethod
    def find_available_reservation_for_table(table,reservations):
        last_lower_timespane = Reservation.start_of_day()
        available_reservations = []
        for reservation in reservations:
            #should we have a minimum time span for reservation, need to ask business about this
            available_reservation = Reservation(table=table,timespan=DateTimeRange(lower=last_lower_timespane,upper=reservation.timespan.lower))
            available_reservations.append(available_reservation)

            last_lower_timespane = reservation.timespan.upper
        
        available_reservations.append(Reservation(table=table,timespan=DateTimeRange(lower=last_lower_timespane,upper=Reservation.end_of_day())))
        return available_reservations

class ReservationToday(generics.ListAPIView):

    queryset = Reservation.objects.filter(timespan__startswith__gte= datetime.now().replace(hour=12,minute=0,second=0,microsecond=0))
    serializer_class = ReservationSerializer
    filter_backends = [restfilters.OrderingFilter]
    ordering_fields = ['timespan']
