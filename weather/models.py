from django.db import models


class City(models.Model):
    city_name = models.CharField(max_length=80)


class Temperatures(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    date = models.DateTimeField('date published')
    temperature = models.IntegerField(default=0)
