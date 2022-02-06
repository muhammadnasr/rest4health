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
    print("============")
    #print(queryset[0].reservation_set[0].id)
    serializer_class = TableSerializer


class ReservationList(generics.ListCreateAPIView):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer


class ReservationDetail(generics.RetrieveDestroyAPIView):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer


class ReservationAvailable(APIView):

    def get(self, request, seats_count, format=None):
        print("test print"+str(seats_count))

        tables = Table.objects.filter(seats_count__lte=seats_count)
        print(tables)
        serializer = TableSerializer(tables, many=True)
        return Response(serializer.data)

"""     def put(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = SnippetSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        snippet = self.get_object(pk)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT) """


