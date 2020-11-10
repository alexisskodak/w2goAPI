from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, generics, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from .models import *
from .serializers import *
import googlemaps
import environ
import json


class ItineraryAPIView(generics.GenericAPIView, mixins.ListModelMixin, mixins.CreateModelMixin):
    serializer_class = ItinerarySerializer
    queryset = Itinerary.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return self.list(request)

    def post(self, request):
        return self.create(request)


class ItineraryDetail(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Itinerary.objects.get(id=pk)
        except Itinerary.DoesNotExist:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, pk):
        itinerary = self.get_object(pk)
        serializer = ItinerarySerializer(itinerary)
        return Response(serializer.data)

    def put(self, request, pk):
        itinerary = self.get_object(pk)
        serializer = ItinerarySerializer(itinerary, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        itinerary = self.get_object(pk)
        itinerary.delete()
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)


class Index(generics.GenericAPIView):
    def get(self, request):
        template_name = 'index.html'
        return render(request, template_name)


env = environ.Env()
environ.Env.read_env(env_file='db.env')
API_KEY = env('API_KEY')
gmaps = googlemaps.Client(key=API_KEY)


def get_places_list(request):
    location = request.GET.get('location')
    keyword = request.GET.get('keyword')
    radius = request.GET.get('radius')
    places_results = gmaps.places_nearby(location=location, keyword=keyword, radius=radius)
    places = places_results['results']
    return places


FIELDS = ['name', 'formatted_address', 'rating', 'type', 'icon', 'photo']
BASE_PHOTO_URL = f'https://maps.googleapis.com/maps/api/place/photo?maxwidth=200&photoreference='


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_places_details(request):
    places_list = get_places_list(request)
    places_details = []
    for place in places_list:
        place_id = place['place_id']
        details = gmaps.place(place_id=place_id, fields=FIELDS)['result']
        details['photos'] = details['photos'][0]['photo_reference']
        places_details.append(details)

    photo_ids = [places_details[i]['photos'] for i in range(len(places_details))]
    photo_urls = [BASE_PHOTO_URL + f'{photo_id}&key={API_KEY}' for photo_id in photo_ids]

    for i in range(len(places_details)):
        places_details[i]['photos'] = photo_urls[i]
    return JsonResponse(places_details, safe=False)
