from django.http.response import JsonResponse
from .models import Guest, Movie, Reservation
from rest_framework.decorators import api_view
from rest_framework import status, filters
from .serializers import GuestSerializers, MovieSerializers, ReservationSerializers
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import Http404
from tickets import serializers

def no_rest_no_model(request):
    jsonlist = []
    # jsonlist.append({'name':'name*6', 'age':99}
    for i in range(22):
        name = chr(65+i)
        age = i
        jsonlist.append({'name':name, 'age':age})

    return JsonResponse(jsonlist, safe=False, json_dumps_params={'ensure_ascii': False})


def no_rest_from_model(request):
    data = Guest.objects.all()
    response = {
        'guests':list(data.values('name', 'age'))
    }
    return JsonResponse(response)


@api_view(['GET', 'POST'])
def FBV_List(request):
    if request.method == 'GET':
        guests = Guest.objects.all()
        serializer = GuestSerializers(guests, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = GuestSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST', 'DELETE'])
def FBV_pk(request, pk):
    try:
        guest = Guest.objects.get(pk=pk)
    except Guest.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = GuestSerializers(guest)
        return Response(serializer.data, status=status.HTTP_200_OK)
    if request.method == 'PUT':
        serializer = GuestSerializers(guest)
        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    if request.method == 'DELETE':
        guest.delete()
        return Response(data={'delete':'successfully'}, status=status.HTTP_200_OK)


class CBV_LIST(APIView):
    def get(self, request):
        guests = Guest.objects.all()
        serializer = GuestSerializers(guests, many=True)
        return Response(serializer.data)
    def post(self, request):
        serializer = GuestSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)

class CBV_pk(APIView):
    def get_ob(self, pk):
        try:
            return Guest.objects.get(pk=pk)
        except Guest.DoesNotExist:
            raise Http404
    def get(self, request, pk):
        guest = self.get_ob(pk)
        serializer = GuestSerializers(guest)
        return Response(serializer.data)
    def put(self, request, pk):
        guest = self.get_ob(pk)
        serializer = GuestSerializers(guest, request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def delete(self, request, pk):
        guest = self.get_ob(pk)
        guest.delete()
        return Response({'Delete':'Successfully'}, status=status.HTTP_200_OK)

