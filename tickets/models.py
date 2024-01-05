from django.db import models

#Guest - Movie - Reservation


class Movie(models.Model):
    hall = models.CharField(max_length=15)
    movie = models.CharField(max_length=15)
    date = models.DateField()

class Guest(models.Model):
    name = models.CharField(max_length=15)
    age = models.IntegerField()   

class Reservation(models.Model):
    guest = models.ForeignKey(Guest, related_name='reservation', on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, related_name='reservation', on_delete=models.CASCADE)
