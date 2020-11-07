from rest_framework import serializers
from .models import *


class StepSerializer(serializers.ModelSerializer):
    class Meta:
        model = Step
        fields = '__all__'


class ItinerarySerializer(serializers.ModelSerializer):
    starting_point = StepSerializer()
    step = StepSerializer()
    ending_point = StepSerializer()

    class Meta:
        model = Itinerary
        fields = '__all__'
