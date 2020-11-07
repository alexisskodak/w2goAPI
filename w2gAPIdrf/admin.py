from django.contrib import admin
from .models import *


@admin.register(Itinerary)
class Itinerary(admin.ModelAdmin):
    class Meta:
        model = Itinerary


@admin.register(Step)
class Step(admin.ModelAdmin):
    pass
