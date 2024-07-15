from django.contrib import admin
from .models import Car, City, DriverCar, BasePrice,BaseTime, BasePercent, BaseTimeRefund

admin.site.register(Car)
admin.site.register(City)
admin.site.register(DriverCar)

admin.site.register(BasePrice)
admin.site.register(BaseTime)

admin.site.register(BasePercent)
admin.site.register(BaseTimeRefund)
