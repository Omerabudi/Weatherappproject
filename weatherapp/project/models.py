from django.db import models
import requests

# Create your models here.
url =""
def updateweather(url):
    response=requests.get(url)
    weather_info=response.json()
    return weather_info



class Favorites(models.Model):
    user_id=models.IntegerField(default=1)
    favorites=models.CharField(max_length=30,default="null")
    class Meta:
        unique_together = (('user_id', 'favorites'),)
    
    def __str__(self):
        return self.favorites



class Weather(models.Model):
    def __init__(self,api_info:dict,location=''):
        self.temp=api_info["main"]["temp"]
        self.temp_min=api_info["main"]["temp_min"]
        self.temp_max=api_info["main"]["temp_max"]
        self.temp_feel=api_info["main"]["feels_like"]
        self.humidity=api_info["main"]["humidity"]
        self.description=api_info['weather'][0]['description']
        self.location=location
    def __str__(self):
        return str(self.__dict__)
    