from django.shortcuts import get_object_or_404
from rest_framework.generics import (
    CreateAPIView,
    RetrieveUpdateDestroyAPIView,
    ListCreateAPIView,
)
from rest_framework import status
from rest_framework.response import Response
from .serializers import (
    DriverCarSerializer,
    CitySerializer,
    CarSerializer,
    BasePriceSerializer,
    BaseTimeSerializer
)
from .models import DriverCar, Car, City, BasePrice, BaseTime
from permissions import IsDriver, IsDriverCar
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAdminUser
from rest_framework import viewsets
from rest_framework import filters
from rest_framework.permissions import IsAuthenticated


class DriverCarCreateView(CreateAPIView):
    """ car choice by driver and post car production date
    """
    queryset = DriverCar.objects.all()
    serializer_class = DriverCarSerializer
    permission_classes = [IsAuthenticated,]
    
    def perform_create(self, serializer):
        driver = self.request.user
        car = self.request.data.get('car')
        driver_exists = DriverCar.objects.filter(driver__user=driver, car=car).exists()
        if driver_exists:
            raise ValidationError('You already registered this car and username!')
        serializer.save(driver__user=driver)
  

class DriverDetailView(viewsets.ViewSet):
    """ driver detail drivers can update self info and delete"""
    queryset = DriverCar.objects.all()
    permission_classes = [IsDriverCar,]
    
    def partial_update(self, request):
        driver = get_object_or_404(self.queryset, driver__user=self.request.user)
        ser_data =  DriverCarSerializer(instance=driver, data=request.POST, partial=True)
        if ser_data.is_valid():
            ser_data.save()
            return Response(ser_data.data, status=status.HTTP_201_CREATED)
        return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request):
        driver = get_object_or_404(self.queryset, driver__user=self.request.user)
        return Response(status=status.HTTP_204_NO_CONTENT)
    

class DriverListView(ListCreateAPIView):
    """ driver list for Admin """
    queryset = DriverCar.objects.all()
    serializer_class = DriverCarSerializer
    permission_classes = [IsAdminUser,]
    filter_backends = [filters.SearchFilter]
    search_fields = ['driver__user__username', 'driver__user__email']
    
            
class CityCreateOrListView(ListCreateAPIView):
    """ add city with lat & lon """
    queryset = City.objects.all()
    serializer_class = CitySerializer
    permission_classes = [IsAdminUser, ]
  
  
class CityDetailView(viewsets.ModelViewSet):
    """ city create, update, delete """
    queryset = City.objects.all()
    serializer_class = CitySerializer
    permission_classes = [IsAdminUser,]
    

class CarRegisterListView(ListCreateAPIView):
    """ add car view by admin"""
    queryset = Car.objects.all()
    serializer_class = CarSerializer
    permission_classes = [IsAdminUser,]
    

class CarDetailView(viewsets.ModelViewSet):
    """ destroy car by admin """
    queryset = Car.objects.all()
    serializer_class = CarSerializer
    permission_classes = [IsAdminUser,]
    

class BasePriceView(ListCreateAPIView):
    """ add base price per kilometer for travel by admin"""
    queryset = BasePrice.objects.all()
    serializer_class = BasePriceSerializer
    # permission_classes = [IsAdminUser,]
    
    def perform_create(self, serializer):
        query = self.queryset.all()
        query.delete()
        serializer.save()
    

class BaseTimeView(ListCreateAPIView):
    """ add base time per kilometer for travel by admin"""
    queryset = BaseTime.objects.all()
    serializer_class = BaseTimeSerializer
    permission_classes = [IsAdminUser,]
    
    def perform_create(self, serializer):
        query = self.queryset.all()
        query.delete()
        serializer.save()

