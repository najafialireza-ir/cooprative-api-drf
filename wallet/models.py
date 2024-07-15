from django.db import models
from accounts.models import User


class Wallet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_wallet')
    balance = models.IntegerField(default=0)
    
    def __str__(self) -> str:
        return self.user.username
    
    def check_credit(self, amount):
        return self.balance >= amount
    
    def deposite(self, amount):
        self.balance += amount
        self.save()
       
    def withdraw(self, amount):
        # if self.check_credit:
        self.balance -= amount
        self.save()

    
class TransectionLog(models.Model):
    choice_list = (('1', 'request'), ('2', 'order'))
    transection_type = models.CharField(choices=choice_list, max_length=5) # question of max length
    log_ids = models.IntegerField()
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name='log_wallet')
    amount = models.IntegerField()
    created = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created',)
    
    def __str__(self) -> str:
        return self.wallet.user.username


class TransectionRequest(models.Model):
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name='request_wallet')
    amount = models.IntegerField()
    is_accepts = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self) -> str:
        return self.wallet.user.username