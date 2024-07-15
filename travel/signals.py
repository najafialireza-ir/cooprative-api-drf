from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import Travel, Ticket
from .models import BaseTime
from datetime import timedelta


@receiver(post_save, sender=Travel)
def create_ticket(sender, instance, created, **kwargs):
    if created:
        capacity = instance.driver_car.car.capacity
        for i in range(1, capacity+1):
            Ticket.objects.create(travel=instance, seat_number=i)
           
    
        
        
