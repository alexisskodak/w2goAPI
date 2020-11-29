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
from .utils import *
import googlemaps
import environ
from urllib.parse import urlencode


env = environ.Env()
environ.Env.read_env(env_file='db.env')


FIELDS = ['name', 'formatted_address', 'rating', 'type', 'icon', 'geometry']
BASE_PHOTO_URL = f'https://maps.googleapis.com/maps/api/place/photo?maxwidth=200&photoreference='
API_KEY = env('API_KEY')
GMAPS = googlemaps.Client(key=API_KEY)


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


def get_location(request):
    if request.method == 'GET' and 'location' in request.GET:
        location = request.GET.get('location')
        return location

    else:
        address = request.GET.get('address')
        if not valid_address(address):
            return HttpResponse(status=status.HTTP_400_BAD_REQUEST)

        result = GMAPS.geocode(address=address)[0]['geometry']['location']
        location = f'{result["lat"]}, {result["lng"]}'
        return location


def get_places(request, location):
    keyword = request.GET.get('keyword')
    radius = request.GET.get('radius')
    if valid_location(location) and valid_keyword(keyword) and radius_in_range(radius):
        results = GMAPS.places_nearby(location=location, keyword=keyword, radius=radius)
        return results['results']
    return


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_places_details(request):
    location = get_location(request)
    if get_places(request, location) is None:
        return HttpResponse(status=status.HTTP_400_BAD_REQUEST)

    steps = [GMAPS.place(place_id=p['place_id'], fields=FIELDS)['result'] for p in get_places(request, location)]

    return JsonResponse(steps, safe=False)


