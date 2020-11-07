from django.urls import path
from .views import *

urlpatterns = [
    path('', Index.as_view(), name='api-home'),
    path('itineraries/', ItineraryAPIView.as_view(), name='api-list'),
    path('itinerary/<int:pk>/', ItineraryDetail.as_view(), name='api-detail')
]
