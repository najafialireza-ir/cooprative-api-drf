from django.urls import path
from . import views


urlpatterns = [
    path('balance/', views.WalletView.as_view()),
    path('request/money/', views.TransectionRequestView.as_view()),    
    path('request/update/<int:pk>/', views.TransectionRequestUpdateView.as_view({'patch': 'partial_update', 'delete': 'destroy'})),
    
    path('user/transection/log/list/', views.TransectionLogListView.as_view()),
    path('user/transection/log/detail/<int:pk>/', views.TransectionLogDetailView.as_view()),
    
]


