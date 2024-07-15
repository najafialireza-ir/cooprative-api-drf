from django.contrib import admin
from .models import Order, PurchasedOrder
# Register your models here.

admin.site.register(Order)
admin.site.register(PurchasedOrder)