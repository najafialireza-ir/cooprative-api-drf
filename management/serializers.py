from rest_framework import serializers
from .models import Car, DriverCar, City, BasePrice, BaseTime
from rest_framework.exceptions import ValidationError
from accounts.serializers import DriverSerializer


class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = ('id', 'name', 'capacity')
    
    def validate(self, data):
        car_exsits = Car.objects.filter(name=data['name'], capacity=data['capacity']).exists()
        if car_exsits:
            raise ValidationError('this car and capacity already exists!!')
        return data
        
         
class DriverCarSerializer(serializers.ModelSerializer):
    driver_obj = DriverSerializer(source='driver', read_only=True)
    car_obj = CarSerializer(source='car', read_only=True)
    class Meta:
        model = DriverCar
        fields = ['id' ,'car','car_obj', 'driver_obj', 'car_production_date']
        read_only_fields = ['id', 'car_obj', 'driver_obj']
        
    
        

class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ('id', 'name', 'lat', 'lon')
        read_only_fields = ["id"]

    def validate(self, data):
        city_exists = City.objects.filter(name=data['name'],
                                          lat=data['lat'], lon=data['lon']).exists()
        if city_exists:
            raise ValidationError('this city already exists!!')
        return data
    
  
class BasePriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = BasePrice
        fields = ('base_price',)
    
    def validate(self, data):
        if data == 0 or data is None:
            raise ValidationError('base_price per kilometer not zero or none!!')
        return data
    
 
class BaseTimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = BaseTime
        fields = ('base_time',)      
    
    def validate(self, data):
        if data == 0 or data is None:
            raise ValidationError('base time per kilometer not zero or none!!')
        return data
    