from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import UserManager
from rest_framework_simplejwt.tokens import RefreshToken


class User(AbstractUser):
    username = models.CharField(max_length=150, unique=False)
    email = models.CharField(max_length=250, unique=True)
    choice = (('1', 'user'),('2', 'driver'),('3', 'admin'))
    user_type = models.CharField(max_length=10, choices=choice)
    is_driver = models.BooleanField(default=False)
    
    objects = UserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['user_type', 'username']
    
    def __str__(self):
        return f'{self.email}'

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }

class Driver(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_driver')
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username}"
    
    

    
    