from django.db import models
from accounts.models import User
from travel.models import Ticket
from .manager import SoftDeleteManager
from django.db.models.signals import pre_delete


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_order')
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    paid_price = models.IntegerField(null=True, blank=True)
    paid_date = models.DateTimeField(auto_now=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)
    
    objects = SoftDeleteManager()
    all_objects = models.Manager()
    
    def __str__(self) -> str:
        return self.user.username
    
    def delete(self):
        pre_delete.send(sender=self.__class__, instance=self)
        self.is_deleted = True
        self.save()
    
    @property
    def get_cost(self):
        return self.ticket.travel.price * self.quantity
    
    
class PurchasedOrder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='p_user')
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='p_order')
    created = models.DateTimeField(auto_now=True)
    
    def __str__(self) -> str:
        return f'{self.user.username}-{self.order.ticket}'
    
    