from rest_framework.generics import (
    ListAPIView, 
    CreateAPIView,
    RetrieveDestroyAPIView,
)
from rest_framework.views import APIView
from .serializers import OrderSerializer, PurchasedSerializer
from .models import Order
from rest_framework.permissions import IsAuthenticated
from permissions import IsOwner
from rest_framework.response import Response
from rest_framework import status
from travel.models import Ticket
from wallet.models import Wallet, TransectionLog
from .models import PurchasedOrder


class OrderListView(ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsOwner,]
    
    def list(self, request, *args, **kwargs):
        user = self.request.user
        orders = self.queryset.filter(user=user)

        if not orders.exists():
            return Response(
                {"error": "You dont have a Order."},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = self.get_serializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AddOrderView(CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer 
    permission_classes = [IsAuthenticated,]
    
    def perform_create(self, serializer):
        user = self.request.user
        ticket_ids = self.request.data.get('ticket_id')
        ticket = Ticket.objects.get(pk=ticket_ids)
        if ticket.status:
            ticket.status = False
            ticket.user = user
            ticket.save()
            serializer.save(user=user, ticket=ticket)
        return Response({'error': 'This ticket alreadu in use.'},
                        status=status.HTTP_404_NOT_FOUND)
    
    
class OrderDetailView(RetrieveDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsOwner,]
    
 
class OrderPayView(APIView):
    permission_classes = [IsOwner,]
    def get(self, request, *args, **kwargs):
        user = self.request.user
        order_query = Order.objects.filter(user=user)
        if not order_query.exists():
            return Response({'message': 'You dont have any order!'}, status=status.HTTP_404_NOT_FOUND)
        wallet_query = Wallet.objects.get(user=user)
        
        for order in order_query:
            product_price = order.get_cost
            check_creadit = wallet_query.check_credit(product_price)
            if check_creadit:
                wallet_query.withdraw(product_price)
                order.paid_price = product_price
                order.save()
                PurchasedOrder.objects.create(user=user, order_id=order.id) # bug
                TransectionLog.objects.create(transection_type='2', wallet=wallet_query, 
                                            amount=(-product_price), log_ids=order.id)
                order.delete()
            else:
                return Response({'message': 'Your wallet balance is Not insufficient!'},
                                status=status.HTTP_400_BAD_REQUEST)
        return Response({'message': 'Successfully paid.'}, status=status.HTTP_200_OK)
    

class PurchasedListView(ListAPIView):
    serializer_class = PurchasedSerializer
    permission_classes = [IsOwner,]

    def get_queryset(self):
        return PurchasedOrder.objects.filter(user=self.request.user)
    

class PurchasedDetailView(RetrieveDestroyAPIView):
    queryset = PurchasedOrder.objects.all()
    serializer_class = PurchasedSerializer
    permission_classes = [IsOwner,]