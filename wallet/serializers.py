from rest_framework import serializers
from .models import Wallet, TransectionLog, TransectionRequest
from rest_framework.exceptions import ValidationError
from accounts.serializers import UserSerializer


class WalletSerializer(serializers.ModelSerializer):
    user_obj = UserSerializer(source='user', read_only=True)
    class Meta:
        model = Wallet
        fields = ('balance', 'user_obj')
        read_only_fields = ('__all__',)
        
    
class TransectionRequestSerializer(serializers.ModelSerializer):
    wallet_obj = WalletSerializer(source='wallet', read_only=True)
    class Meta:
        model = TransectionRequest
        fields = ('id', 'wallet', 'amount','is_accepts', 'created', 'wallet_obj')
        read_only_fields = ('id','wallet', 'is_accepts', 'created', 'wallet_obj')
        
    def validate(self, value):
        if value['amount'] == 0 or value['amount'] is None:
            raise ValidationError('Amount can`t be zero or empty!')
        return value
    

class TransectionRequestListSerializer(serializers.ModelSerializer):
    wallet_obj = WalletSerializer(source='wallet', read_only=True)
    class Meta:
        model = TransectionRequest
        fields = ('id', 'amount', 'wallet', 'is_accepts', 'created', 'wallet_obj')
        read_only_fields = ('id', 'wallet', 'created', 'wallet_obj',)
        extra_kwargs = {'amount': {'required': False}} 
        

class TransectionLogSerializer(serializers.ModelSerializer):
    wallet_obj = WalletSerializer(source='wallet', read_only=True)
    class Meta:
        model = TransectionLog
        fields = ('__all__')
        read_only_fields = ('__all__',)
        
