from rest_framework import serializers
from .models import Order, PurchasedOrder
from rest_framework.exceptions import ValidationError
from travel.models import Ticket, Travel
from accounts.serializers import UserSerializer
from management.serializers import DriverCarSerializer, CitySerializer


class TravelCustomSerializer(serializers.ModelSerializer):
    driver_car_obj = DriverCarSerializer(source='driver_car', read_only=True)
    start_city_obj = CitySerializer(source='start_city', read_only=True) 
    destination_city_obj = CitySerializer(source='start_city', read_only=True) 
    
    class Meta:
        model = Travel 
        fields = ('driver_car_obj', 'start_city_obj', 'destination_city_obj', 'date_time', 'end_time', 'price')


class TicketCustomSerializer(serializers.ModelSerializer):
    travel_obj = TravelCustomSerializer(source='travel', read_only=True)
    
    class Meta:
        model = Ticket
        fields = ('status', 'seat_number', 'created', 'travel_obj')


class OrderSerializer(serializers.ModelSerializer):
    ticket_obj = TicketCustomSerializer(source='ticket', read_only=True)
    user_obj = UserSerializer(source='user', read_only=True)
    ticket_id = serializers.IntegerField()
    get_cost = serializers.SerializerMethodField()
    
    class Meta:
        model = Order
        fields = ('id', 'quantity', 'created', 'ticket_id', 'ticket_obj', 'user_obj', 'get_cost')
        read_only_fields = ('get_cost',)
    def validate_quantity(self, value):
        if value != 1:
            raise ValidationError('quantity must be exactly 1 !!')
        return value
    
    def validate_ticket_id(self, value): 
        ticket_exists = Ticket.objects.filter(pk=value, status=False).exists()
        if ticket_exists:
            raise ValidationError('This ticket already in use!')
        return value

    def get_cost(self, obj):
        return obj.get_cost
   
class PurchasedSerializer(serializers.ModelSerializer):
    user_obj = UserSerializer(source='user', read_only=True)
    order_obj = OrderSerializer(source='order', read_only=True)
    class Meta:
        model = PurchasedOrder
        fields = ('__all__')
        