from rest_framework.generics import CreateAPIView
from .serializers import UserSerializer, UserProfileSerializer, DriverProfileSerializer, LogoutSerializer, LoginSerializer
from rest_framework.response import Response
from rest_framework import status
from .models import User, Driver
from rest_framework.permissions import IsAuthenticated
from management.models import DriverCar
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import viewsets      
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from django.http import HttpResponse
import xlwt
from rest_framework.permissions import IsAdminUser


class UserRegisterView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        validated_data = serializer.validated_data
        del validated_data['password2']
        user_type = validated_data['user_type']
        
        if user_type == '1':
            user = User.objects.create_user(**validated_data)
        elif user_type == '2':
            cd = validated_data
            user = User.objects.create_driver(username=cd['username'], email=cd['email'], user_type=cd['user_type'], password=cd['password'])
            driver = Driver.objects.create(user=user)
            DriverCar.objects.create(driver=driver, car=cd.get('driver_car', {}).get('car', {}),
                                     car_production_date=cd.get('driver_car', {}).get('car_production_date', {}))
        elif user_type == '3':
            user = User.objects.create_superuser(**validated_data)
        serializer.instance = user
        
  
# class UserProfileView(viewsets.ModelViewSet):
#     queryset = User.objects.all()
#     serializer_class = UserProfileSerializer 
#     permission_classes = [IsAuthenticated,]  
    
#     def get_object(self):
#         return self.request.user

#     def partial_update(self, request, *args, **kwargs):
#         try:
#             user = self.queryset.get(pk=self.request.user.id)
#         except User.DoesNotExist:
#             return Response(status=status.HTTP_404_NOT_FOUND)
      
#         serializer = self.get_serializer_class(instance=user, data=request.data, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class UserProfileView(viewsets.ViewSet):
    """ if normal user: Fields=('id', 'username', 'email'),
    elif driver: Fields= ['driver', 'car', 'car_production_date', 'driver_obj', 'car_obj', 'username', 'email']"""
    
    permission_classes = [IsAuthenticated,]

    def get_serializer_class(self):
        if self.action in ('list', 'partial_update'):
            if self.request.user.is_driver:
                return DriverProfileSerializer
            return UserProfileSerializer
        raise MethodNotAllowed(self.action)
        
    def get_object(self):
        try:
            if self.request.user.is_driver:
                return DriverCar.objects.get(driver__user=self.request.user)
            return User.objects.get(email=self.request.user.email)
        except (User.DoesNotExist, DriverCar.DoesNotExist):
            return None

    def list(self, request):
        obj = self.get_object()
        if obj is None:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(obj)
        return Response(serializer.data)

    @extend_schema(
        request=UserProfileSerializer,
        responses={200: UserProfileSerializer})
    def partial_update(self, request, pk=None):
        obj = self.get_object()
        if obj is None:
            return Response({'error': 'User or DriverCar not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(obj, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(GenericAPIView):
    serializer_class = LoginSerializer
    
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserLogoutView(GenericAPIView):
    serializer_class = LogoutSerializer
    permission_classes = (IsAuthenticated,)
    
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserExportExcel(APIView):
    permission_classes = [IsAdminUser]
    
    def get(self, request):
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="users.xls"'
        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet('Users')

        # Sheet header, first row
        row_num = 0

        font_style = xlwt.XFStyle()
        font_style.font.bold = True

        columns = ['Username', 'Email address', 'UserType']

        # start by index and row number
        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num], font_style)

        # Sheet body, remaining rows
        font_style = xlwt.XFStyle()

        #convert to list and itrate
        users = User.objects.all().values_list('username', 'email', 'user_type')
        for row in users:
            row_num += 1
            for col_num in range(len(row)):
                ws.write(row_num, col_num, row[col_num], font_style)

        wb.save(response)
        return response
    