from .models import Travel, Ticket
from rest_framework.permissions import IsAdminUser
from management.models import DriverCar
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import (
    ListAPIView,
)
from rest_framework import viewsets
from .serializers import (TravelSerializer,
    TravelCreateByDriverSerializer,
    TicketAllInfoSerializer,
    TicketPartInfoSerializer,
    TravelInstanceSerializer,
)
from permissions import IsAdminOrIsDriverWriteOnly
from rest_framework.exceptions import ValidationError, PermissionDenied
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import filters
from rest_framework.permissions import IsAuthenticated
import xlwt
from django.http import HttpResponse
import datetime  


@extend_schema_view(
    create=extend_schema(
        request=TravelSerializer,
        responses={201: TravelSerializer, 400: 'Bad Request'},))
class TravelListOrCreateView(viewsets.ModelViewSet):
    """ 
    if Driver create travel must be write (start_city, destination_city, date_time(start_time)),
    but admin create travel select driver,
    driver can`t change or write driver field
    """
    filter_backends = [filters.SearchFilter,]
    search_fields = ['start_city__name', 'driver_car__car__name', 'created']
    
    def get_permissions(self):
        if self.action == 'list':
            permission_classes = []
        else:
            permission_classes = [IsAdminOrIsDriverWriteOnly] 
        return [permission() for permission in permission_classes]
    
    def get_queryset(self):
        queryset = Travel.objects.all()
        if self.request.user.is_authenticated and self.request.user.is_driver:
            driver_queryset = queryset.filter(driver_car__driver=self.request.user.user_driver)
            return driver_queryset
        return queryset
    
    def get_serializer_class(self):
        if self.action == 'create':
            if self.request.user.is_authenticated:
                if self.request.user.is_superuser:
                    return TravelSerializer
                else:
                    return TravelCreateByDriverSerializer
            raise PermissionDenied({'messages':'you must authentication!'})
        return TravelSerializer

    def perform_create(self, serializer):
        if not self.request.user.is_superuser:
            driver_car = DriverCar.objects.get(driver__user=self.request.user)
        else:
            driver_car = serializer.validated_data.get('driver_car')

        start_city = serializer.validated_data['start_city']
        date_time = serializer.validated_data['date_time']
        destination_city = serializer.validated_data['destination_city']
        if start_city == destination_city:
            raise ValidationError({'messages': 'Start city and destination city cannot be the same!'})

        travel = Travel(driver_car=driver_car, start_city=start_city, destination_city=destination_city, date_time=date_time)

        if travel.get_distance != 0:
            travel.end_time = travel.get_distance_time
            travel.price = travel.get_cost
            travel.capacity = travel.driver_car.car.capacity

        is_travel_exists = Travel.objects.filter(driver_car=travel.driver_car, 
                                                 date_time__range=[travel.date_time, travel.end_time]).exists()
        if is_travel_exists:
            raise ValidationError({'messages': 'Driver is on travel at this time.'})
        travel.approved = self.request.user.is_superuser
        serializer.save(driver_car=driver_car, capacity=travel.capacity, approved=travel.approved, end_time=travel.end_time,
                        price=travel.price) 

 
class TravelRequestListView(ListAPIView):
    queryset = Travel.objects.filter(approved=False)
    serializer_class = TravelSerializer
    permission_classes = [IsAdminUser,]


class TravelUpdateView(viewsets.ModelViewSet): 
    permission_classes = [IsAdminUser,]
    def partial_update(self, request, pk):
        try:
            travel_instance = Travel.objects.get(pk=pk)
        except Travel.DoesNotExist:
            return Response(ser_data.errors, status=status.HTTP_404_NOT_FOUND)
        
        ser_data = TravelInstanceSerializer(instance=travel_instance, data=request.POST, partial=True)
        if ser_data.is_valid():
            ser_data.save()
            return Response(ser_data.data, status=status.HTTP_201_CREATED)
        return Response(ser_data.errors, status=status.HTTP_404_NOT_FOUND)
    
    def destroy(self, request, pk):
        try:
            queryset = Travel.objects.get(pk=pk)
        except Travel.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        queryset.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    
class TicketListView(APIView):
    """ show ticket list with travel_id and send query_param get ticket list status=True or False
    if superuser: Fields=('id', 'status', 'created', 'seat_number', 'travel_obj', 'user_obj')
    or noemal user Fields = ('id', 'status', 'seat_number', 'travel_obj',)"""
    
    permission_classes = [IsAuthenticated,]
    def get(self, request, pk):
        if request.user.is_superuser:
            ticket = Ticket.objects.filter(travel_id=pk)
            search = request.GET.get('search', None)
            if search:
               ticket = ticket.filter(status=search)
            ser_data = TicketAllInfoSerializer(instance=ticket, many=True)
            return Response(ser_data.data, status=status.HTTP_200_OK)
        else:
            ticket = Ticket.objects.filter(travel_id=pk)
            ser_data = TicketPartInfoSerializer(instance=ticket, many=True)
            return Response(ser_data.data, status=status.HTTP_200_OK)
        

class TravelDetailView(viewsets.ModelViewSet):
    """ can delete travel if superuser """
    permission_classes = [IsAdminUser,]
    queryset = Travel.objects.all()
    serializer_class = TravelSerializer

    
class TravelExportExcel(APIView):
    permission_classes = [IsAdminUser]
    
    def get(self, request):
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="travels.xls"'

        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet('Travels')

        # Sheet header, first row
        row_num = 0

        font_style = xlwt.XFStyle()
        font_style.font.bold = True

        columns = ['driver_car', 'start_city', 'destination_city',
                   'date_time', 'end_time', 'capacity', 'price']

        # start by index and row number
        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num], font_style)

        # Sheet body, remaining rows
        font_style = xlwt.XFStyle()

        #convert to list and itrate
        travels = Travel.objects.all().values_list('driver_car__driver__user__username', 'start_city__name', 'destination_city__name',
                                                    'date_time', 'end_time', 'capacity', 'price')
        
        for row in travels:
            row_num += 1
            for col_num in range(len(row)):
                if isinstance(row[col_num], datetime.datetime):
                    date_time = row[col_num].strftime('%Y-%m-%d %H:%M:%S')
                    ws.write(row_num, col_num, date_time, font_style)
                else:
                    ws.write(row_num, col_num, row[col_num], font_style)

        wb.save(response)
        return response
    