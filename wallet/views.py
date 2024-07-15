from rest_framework.views import APIView
from rest_framework.generics import (
    RetrieveDestroyAPIView,
    ListCreateAPIView,
    ListAPIView,
    
)
from .models import Wallet, TransectionRequest, TransectionLog
from .serializers import (WalletSerializer,
    TransectionLogSerializer,
    TransectionRequestSerializer,
    TransectionRequestListSerializer
)
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework import status
from permissions import IsOwner, IsOwnerTransection
from rest_framework import viewsets


class WalletView(APIView):
    permission_classes = [IsOwner,]
    serializer_class = WalletSerializer
    
    def get(self, request):
        wallet = Wallet.objects.filter(user=request.user)
        ser_data = self.serializer_class(instance=wallet, many=True)
        return Response(ser_data.data, status=status.HTTP_200_OK)
    
    
class TransectionRequestView(ListCreateAPIView):
    """ if user request return user transection,
    if admin request return transections (is_accepts=False) """
    
    serializer_class = TransectionRequestSerializer
    permission_classes = [IsAuthenticated,]
       
    def get_queryset(self):
        if not self.request.user.is_superuser:
            transection_query = TransectionRequest.objects.filter(wallet=self.request.user.user_wallet)
            return transection_query
        else:
            search = self.request.GET.get('search', None)
            transection_query = TransectionRequest.objects.all()
            if search:
                transection_query = transection_query.filter(is_accepts=search)
                return transection_query
            return transection_query
     
    def perform_create(self, serializer):
        wallet = self.request.user.user_wallet
        serializer.save(wallet=wallet)  
        

class TransectionRequestUpdateView(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser,]
    def partial_update(self, request, pk):
        try:
            queryset = TransectionRequest.objects.get(pk=pk)
        except TransectionRequest.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        ser_data = TransectionRequestListSerializer(instance=queryset, data=request.data)
        if ser_data.is_valid():
            ser_data.save()
            return Response(ser_data.data, status=status.HTTP_201_CREATED)
        return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request, pk):
        try:
            queryset = TransectionRequest.objects.get(pk=pk)
        except TransectionRequest.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        queryset.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

class TransectionLogListView(ListAPIView):
    """ users read self transections """
    
    queryset = TransectionLog.objects.all()
    serializer_class = TransectionLogSerializer
    permission_classes = [IsOwnerTransection,]
    
    def get_queryset(self):
        user = self.request.user
        try:
            queryset = self.queryset.filter(wallet__user=user)
        except TransectionLog.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return queryset
        

class TransectionLogDetailView(RetrieveDestroyAPIView):
    queryset = TransectionLog.objects.all()
    serializer_class = TransectionLogSerializer
    permission_classes = [IsOwnerTransection,]

    def destroy(self, request, pk=None):
        user = self.request.user
        try:
            query = self.queryset.filter(pk=pk, wallet__user=user)
        except TransectionLog.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        query.delete()
        return Response({'message':'Transection deleted!!'}, status=status.HTTP_204_NO_CONTENT)