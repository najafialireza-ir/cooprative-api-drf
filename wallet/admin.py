from django.contrib import admin
from .models import Wallet, TransectionLog, TransectionRequest


admin.site.register(Wallet)
admin.site.register(TransectionLog)
admin.site.register(TransectionRequest)
