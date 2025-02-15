from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
# Create your models here.
# class User(AbstractUser):
#     phone_number = models.CharField(max_length=15, blank=True, null=True)

#     def __str__(self):
#         return self.username
class User(AbstractUser):
    # Add custom fields if needed
    pass


class Image(models.Model):
    name = models.CharField(max_length=255)
    url = models.TextField(default="")
    slug = models.TextField(default="")
    createdAt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
class Airline(models.Model):
    createdAt = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=255)
    price = models.FloatField(default=0.0)
    destinationID = models.ForeignKey('Destination', on_delete=models.CASCADE)
    rating = models.FloatField(default=0.0)
    timeTaken = models.FloatField(default=0.0)
    remarks = models.TextField(default="")

class Hotel (models.Model):
    createdAt = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=255)
    price = models.FloatField(default=0.0)
    destinationID = models.ForeignKey('Destination', on_delete=models.CASCADE)
    rating = models.FloatField(default=0.0)
    anemeties = models.TextField(default="")
    remarks = models.TextField(default="")


class Bus(models.Model):
    createdAt = models.DateTimeField(auto_now_add=True) 
    name = models.CharField(max_length=255)
    price = models.FloatField(default=0.0)
    destinationID = models.ForeignKey('Destination', on_delete=models.CASCADE)
    rating = models.FloatField(default=0.0)
    timeTaken = models.FloatField(default=0.0)
    remarks = models.TextField(default="")
    
class Destination(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    destination_type = models.CharField(
        max_length=50, 
        choices=[('Local', 'Local'), ('International', 'International')],
        default= 'Local'
    )
    longitude = models.FloatField(default=0.0)
    latitude = models.FloatField(default=0.0)
    location = models.CharField(max_length=255)
    image = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    popularity = models.FloatField(default=0.0)

    def __str__(self):
        return self.name
    
class TravelCost(models.Model):
    destinationID = models.ForeignKey(Destination, on_delete=models.CASCADE)
    userID = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    price = models.FloatField(default=0.0)
    start_date = models.DateField()
    end_date = models.DateField()


from .models import Destination
class TravelPlan(models.Model):
    destination = models.ForeignKey('Destination', on_delete=models.CASCADE)
    food_type = models.CharField(max_length=50, choices=[('Veg', 'Veg'), ('Non-Veg', 'Non-Veg')])
    lodging = models.CharField(max_length=50, choices=[('Hotel', 'Hotel'), ('Lodge', 'Lodge'), ('Resort', 'Resort')])
    individual_count = models.PositiveIntegerField(default=1)
    start_date = models.DateField()
    end_date = models.DateField()
    total_cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    pricing_segment = models.CharField(max_length=50, null=True, blank=True)
    travel_options = models.JSONField(null=True, blank=True)


    def __str__(self):
        return f"TravelPlan for {self.destination.name}"