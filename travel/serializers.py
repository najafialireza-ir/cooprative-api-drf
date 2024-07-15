from rest_framework import serializers
from .models import Travel, Ticket
from rest_framework.exceptions import ValidationError
from management.serializers import DriverCarSerializer, CitySerializer
from accounts.serializers import UserSerializer
from management.serializers import CitySerializer


class TravelSerializer(serializers.ModelSerializer):
    distance = serializers.SerializerMethodField()
    driver_car_obj = DriverCarSerializer(source='driver_car', read_only=True)
    start_city_obj = CitySerializer(source='start_city', read_only=True)
    destination_city_obj = CitySerializer(source='destination_city', read_only=True)
    capacity = serializers.SerializerMethodField()
    
    class Meta:
        model = Travel
        fields = ('id', 'driver_car', 'start_city', 'destination_city', 'distance', 'date_time', 'end_time',
                  'capacity', 'driver_car_obj', 'start_city_obj', 'destination_city_obj')
        read_only_fields = ('id', 'end_time', 'price','distance', 'driver_car_obj', 'start_city_obj', 'destination_city_obj',
                            'capacity')
        
    def validate(self, data):
        date_time = data.get('date_time')
        driver_car = data.get('driver_car')
        start_city = data.get('start_city')
        destination_city = data.get('destination_city')
        if not all([date_time, driver_car, start_city, destination_city]):
            raise ValidationError('required fields: date_time, driver_car, start_city, destination_city')
        return data
    
    def get_distance(self, obj):
        return obj.get_distance
    
    def get_capacity(self, obj):
        return obj.get_remaind_capacity
    
    
class TravelCreateByDriverSerializer(serializers.ModelSerializer):
    start_city_obj = CitySerializer(source='start_city', read_only=True)
    destination_city_obj = CitySerializer(source='destination_city', read_only=True)
    
    class Meta:
        model = Travel
        fields = ('approved', 'start_city', 'destination_city', 'date_time', 'start_city_obj', 'destination_city_obj')
        read_only_fields = ('approved',)
        
        
class TravelInstanceSerializer(serializers.ModelSerializer):
    start_city_obj = CitySerializer(source='start_city', read_only=True)
    destination_city_obj = CitySerializer(source='destination_city', read_only=True)
    
    class Meta:
        model = Travel
        fields = ('approved', 'start_city', 'destination_city', 'date_time', 'start_city_obj', 'destination_city_obj')
       
        
class TicketAllInfoSerializer(serializers.ModelSerializer):
    travel_obj = TravelSerializer(source='travel', read_only=True)
    user_obj = UserSerializer(source='user', read_only=True)
    
    class Meta:
        model = Ticket
        fields = ('id', 'status', 'created', 'seat_number', 'travel_obj', 'user_obj')
        
    def validate(self, data):
        date_time = data.get('date_time')
        start_city = data.get('start_city')
        destination_city = data.get('destination_city')
        if not all([date_time, start_city, destination_city]):
            raise ValidationError('required fields: date_time, start_city, destination_city')
        return data


class TicketPartInfoSerializer(serializers.ModelSerializer):
    travel_obj = TravelSerializer(source='travel', read_only=True)
    
    class Meta:
        model = Ticket
        fields = ('id', 'status', 'seat_number', 'travel_obj',)
        
        
