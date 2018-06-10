from django.db import models
from django.utils import timezone 
import datetime
 

class User(models.Model):
    user_id = models.IntegerField()
    username = models.CharField(max_length=200)
    sex = models.TextField()
    age = models.IntegerField()
    location_id = models.IntegerField()
    favorite = models.TextField()
    favorite_code = models.IntegerField()
    address = models.TextField()
 
class Cafe(models.Model):
    cafe_id =models.IntegerField()
    cafe_name =models.TextField()
    cafe_address = models.TextField()
    location_id = models.IntegerField()
    opentime = models.DateTimeField()
    closetime = models.DateTimeField()
    image_url = models.TextField()

class Location(models.Model):
    location_id =models.IntegerField()
    address = models.TextField()

class Coupon(models.Model):
    user_id =models.IntegerField()
    cafe_name =models.TextField()
    count =models.IntegerField()

class menu(models.Model):
    cafe_id =models.IntegerField()
    menu_name = models.TextField()
    price =models.IntegerField()
    menu_code=models.IntegerField()

class Log(models.Model):
    cafe_id = models.IntegerField()
    day = models.DateTimeField()
    time = models.DateTimeField()
    user_num = models.IntegerField()