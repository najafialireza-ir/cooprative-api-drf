from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from accounts.models import User
from .models import Wallet, TransectionRequest, TransectionLog


@receiver(post_save, sender=User)
def create_user_wallet(sender, instance, created, **kwargs):
    if created:
        Wallet.objects.create(user=instance)
        

@receiver(pre_save, sender=TransectionRequest)
def add_amount_wallet(sender, instance, raw, **kwargs):
    try:
        old_instance = TransectionRequest.objects.get(id=instance.id)
        wallet = instance.wallet
        amount = instance.amount
        if instance.is_accepts and not old_instance.is_accepts:
            wallet.deposite(amount)
            TransectionLog.objects.create(transection_type='1', log_ids=instance.id, wallet=wallet, amount=amount)
        elif not instance.is_accepts and old_instance.is_accepts:
            wallet.withdraw(amount)
            TransectionLog.objects.create(transection_type='1', log_ids=instance.id, wallet=wallet, amount=-amount)
        wallet.save()
    except:
        pass
    

