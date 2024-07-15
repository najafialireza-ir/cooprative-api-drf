from rest_framework import serializers
from .models import User, Driver
from rest_framework.exceptions import ValidationError
from management.models import DriverCar, Car

 
class UserSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(required=True, write_only=True)
    class Meta:
        model = User
        fields = ('id' ,'username', 'email', 'user_type', 'password', 'password2')
        extra_kwargs = {
            'password': {'write_only': True}
        }
    
    def validate_email(self, value):
        if '@' not in value:
            raise serializers.ValidationError("Email address must contain '@'.")
        if '.com' not in value:
            raise serializers.ValidationError("Email address must contain '.com'.")
        return value
        
    def validate(self, data):
        username = data.get('username')
        email = data.get('email')
        email_exists = User.objects.filter(email=email).exists()
        if email_exists:
            raise serializers.ValidationError("This email is already in use.")
        elif not all([username, email]):
            raise ValidationError('required field: username, email')
        return data   
    
    
    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError('password must be matches!')
        return data
    
    
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')
        read_only_fields = ('id',)
    
    def validate_email(self, value):
        """ check if the email is valid and not already in use. """
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("This email is already in use.")
        return value   


class DriverSerializer(serializers.ModelSerializer):
    user_obj = UserProfileSerializer(source='user', read_only=True)
    class Meta:
        model = Driver
        fields = ('id', 'user', 'created', 'user_obj')
        
        
class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = ('id', 'name', 'capacity')    


class DriverProfileSerializer(serializers.ModelSerializer):
    driver_obj = DriverSerializer(source='driver')
    car_obj = CarSerializer(source='car', read_only=True)
    username = serializers.CharField(source='driver.user.username')
    email = serializers.EmailField(source='driver.user.email')
    
    class Meta:
        model = DriverCar
        fields = ['driver', 'car', 'car_production_date', 'driver_obj', 'car_obj', 'username', 'email']

    def update(self, instance, validated_data):
        user_data = validated_data.pop('driver', {}).get('user', {})             
        user = instance.driver.user
                
        if 'username' in user_data:
            user.username = user_data['username']
        if 'email' in user_data:
            user.email = user_data['email']
        user.save()
        
        # update drivercar fields 
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance