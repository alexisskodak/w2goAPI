from django.db import models


class Step(models.Model):
    address = models.CharField(max_length=128, default='')
    latitude = models.FloatField(default=0)
    longitude = models.FloatField(default=0)
    name = models.CharField(max_length=48, default='')
    category = models.CharField(max_length=24, blank=True, null=True)
    rating = models.IntegerField(blank=True, null=True)
    description = models.CharField(max_length=256, blank=True, null=True)

    def __str__(self):
        return self.name


class Itinerary(models.Model):
    starting_point = models.ForeignKey(Step, on_delete=models.DO_NOTHING, related_name='itinerary_startp')
    step = models.ForeignKey(Step, on_delete=models.DO_NOTHING, related_name='itinerary_midp')
    ending_point = models.ForeignKey(Step, on_delete=models.DO_NOTHING, related_name='itinerary_endp')

    def __str__(self):
        return 'From: ' + self.starting_point.name + '. To: ' + self.ending_point.name

    class Meta:
        verbose_name_plural = 'Itineraries'


