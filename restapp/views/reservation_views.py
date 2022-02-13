
from restapp.models import Reservation, Table
from restapp.serializers import ReservationSerializer
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from psycopg2.extras import DateTimeRange
from rest_framework import generics
from rest_framework import filters 
from rest_framework import permissions
from rest_framework.decorators import permission_classes

class ReservationAvailable(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, seats_count, format=None):

        available_reservations = []
        #to maximize profit we look for tables with exact max seats and if we didn't find any slot, 
        #we look for seats+1 and so on
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
    permission_classes = [permissions.IsAuthenticated]

    queryset = Reservation.objects.filter(timespan__startswith__gte= Reservation.start_of_day())
    serializer_class = ReservationSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['timespan']


class ReservationList(APIView):

    def get_permissions(self):
        """
        Handling customer persmissions be method is not straigt forward and the documentation example is simply not working
        """
        if self.request.method == 'POST':
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [permissions.IsAdminUser]
        return [permission() for permission in permission_classes]

    def get(self, request, format=None):

        #we had to implement filtering manually as DateTimeRangeFilter with Django rest (even with custom filters)
        table =request.GET.get('table')
        from_datetime =request.GET.get('from')
        to_datetime =request.GET.get('to')

        reservations = Reservation.objects.all()
        if table:
            reservations = reservations.filter(table=table)

        if from_datetime:
            reservations = reservations.filter(timespan__startswith__gte=from_datetime)

        if to_datetime:
            reservations = reservations.filter(timespan__endswith__lte=to_datetime)

        serializer = ReservationSerializer(reservations, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        permission_classes = [permissions.IsAuthenticated]
        serializer = ReservationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)   
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ReservationDetail(generics.DestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer