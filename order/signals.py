from django.db.models.signals import post_save, pre_save, pre_delete
from django.dispatch import receiver
from .models import Order, PurchasedOrder
from travel.models import Ticket
from management.models import BaseTimeRefund, BasePercent
from datetime import timedelta, datetime
from wallet.models import Wallet, TransectionLog


@receiver(pre_delete, sender=Order)
def return_paid_price(instance, sender, **kwargs):
    ticket = Ticket.objects.get(id=instance.ticket.id)
    paid_price = instance.paid_price
    try:
        if paid_price:
            ticket.status = False
            ticket.user = instance.user
            ticket.save()
        else:
            ticket.status = True
            ticket.user = None
            ticket.save()
    except:
        pass 


@receiver(pre_delete, sender=PurchasedOrder)
def return_ticket(sender, instance, **kwargs):
    ticket = Ticket.objects.get(id=instance.order.ticket.id)
    paid_price = instance.order.paid_price
    
    base_time_refund = BaseTimeRefund.objects.all().last()
    now_time = datetime.now()
    paid_date_time = instance.order.paid_date
    result = (now_time - paid_date_time)
    wallet =  Wallet.objects.get(user=instance.uesr)
    
    if result > timedelta(seconds=base_time_refund.base_time):
        percent = BasePercent.objects.all().last()
        deducted_amount = (percent / 100) * paid_price
        result  = int(paid_price - deducted_amount)
        wallet.deposite(result)
        wallet.save()
        ticket.is_available = True
        ticket.user = None
        ticket.save()
        TransectionLog.objects.create(transection_type='2', wallet=wallet, 
                                            amount=result, log_ids=instance.order.id)
    else:
        wallet.deposite(paid_price)
        wallet.save()  
        ticket.is_available = True
        ticket.user = None
        ticket.save()
        TransectionLog.objects.create(transection_type='2', wallet=wallet, 
                                            amount=paid_price, log_ids=instance.order.id)

