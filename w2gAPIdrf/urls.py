from django.urls import path, re_path
from .views import *


location_pattern = r'^[-+]?([1-8]?\d(\.\d+)?|90(\.0+)?),\s*[-+]?(180(\.0+)?|((1[0-7]\d)|([1-9]?\d))(\.\d+)?)$'

urlpatterns = [
    path('', Index.as_view(), name='api-home'),
    path('api/itineraries/', ItineraryAPIView.as_view(), name='api-list'),
    path('api/itinerary/<int:pk>/', ItineraryDetail.as_view(), name='api-detail'),
    path('api/gmaps-places/', get_places_details, name='places-by-location'),
]
