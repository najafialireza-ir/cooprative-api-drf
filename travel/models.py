from django.db import models
from management.models import DriverCar
from accounts.models import User
import haversine as hs
from haversine import Unit
from management.models import City
from management.models import BaseTime
from datetime import timedelta
from management.models import BasePrice


class Travel(models.Model):
    driver_car = models.ForeignKey(DriverCar, on_delete=models.CASCADE, related_name='travel_driver_car')
    start_city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='start_city')
    destination_city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='des_city')
    date_time = models.DateTimeField()
    end_time = models.DateTimeField(null=True, blank=True)
    capacity = models.PositiveSmallIntegerField()
    approved = models.BooleanField(default=False)
    price = models.IntegerField(null=True, blank=True)
    
    class Meta:
        ordering = ('-date_time',)
    
    def __str__(self) -> str:
        return f'{self.driver_car}-{self.start_city}-{self.destination_city}'
    
    @property
    def get_distance(self):
        city_1 = self.start_city
        city_2 = self.destination_city
        if not (city_1 or city_2):
            return 0
        loc1 = (city_1.lat, city_1.lon)
        loc2 = (city_2.lat, city_2.lon)
        result = hs.haversine(loc1,loc2, unit=Unit.KILOMETERS)
        return int(result)
        
    @property  
    def get_distance_time(self):
        obj = BaseTime.objects.all().last()
        if obj:
            cal_time = obj.base_time * self.get_distance
            arrival_time = self.date_time + timedelta(seconds=cal_time)
            return arrival_time

    @property
    def get_cost(self):
        obj = BasePrice.objects.all().last()
        return obj.base_price * self.get_distance
    
    @property
    def get_remaind_capacity(self):
        try:
            user = Ticket.objects.filter(travel=self, user__isnull=False).count()
            count_quantity = self.capacity - user
            return count_quantity
        except:
            return self.capacity
        
    
class Ticket(models.Model):
    travel = models.ForeignKey(Travel, on_delete=models.CASCADE, related_name='ticket_travel')
    user =  models.ForeignKey(User, on_delete=models.CASCADE, related_name='ticket_user', null=True, blank=True)
    status = models.BooleanField(default=True)
    seat_number = models.IntegerField()
    created = models.DateField(auto_now_add=True)
    
    def __str__(self) -> str:
        return f'{self.travel.start_city}-{self.travel.destination_city}-{self.travel.date_time}'
    