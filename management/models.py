from django.db import models
from accounts.models import Driver


class Car(models.Model):
    name = models.CharField(max_length=50)
    capacity = models.IntegerField()
    
    def __str__(self) -> str:
        return f"{self.name}-{self.capacity}"
    

class DriverCar(models.Model):
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE, related_name='driver_car')
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    car_production_date = models.DateField()
    
    def __str__(self) -> str:
        return f'{self.driver}-{self.car}'
    
    
class City(models.Model):
    name = models.CharField(max_length=50)
    lat = models.FloatField()
    lon = models.FloatField()
    
    def __str__(self) -> str:
        return f'{self.name}'
    

class BaseTime(models.Model):
    base_time = models.IntegerField()
    
class BasePrice(models.Model):
    base_price = models.IntegerField()


class BasePercent(models.Model):
    base_percent = models.IntegerField()
    created = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return str(self.base_percent)
    

class BaseTimeRefund(models.Model):
    base_time = models.PositiveIntegerField()
    created = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return str(self.base_time)
    