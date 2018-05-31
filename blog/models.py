from django.db import models
from django.utils import timezone 
 

class User(models.Model):
    user_id = models.IntegerField()
    username = models.CharField(max_length=200)
    sex = models.TextField()
    age = models.IntegerField()
    location_id = models.IntegerField()
 
class Cafe(models.Model):
    cafe_id =models.IntegerField()
    cafe_name =models.TextField()
    cafe_address = models.TextField()
    location_id = models.IntegerField()
    opentime = models.TextField()
    closetime = models.TextField()
    image_url = models.TextField()

class Location(models.Model):
    location_id =models.IntegerField()
    address = models.TextField()

class Coupon(models.Model):
    user_id =models.IntegerField()
    cafe_id =models.IntegerField()
    count =models.IntegerField()

class menu(models.Model):
    cafe_id =models.IntegerField()
    menu_name = models.TextField()
    price =models.IntegerField()
    menu_code=models.IntegerField()