from django.urls import path
from . import views

urlpatterns = [
    path('list/', views.OrderListView.as_view()),
    path('detail/<int:pk>/', views.OrderDetailView.as_view()),
    path('add/', views.AddOrderView.as_view()),
    path('pay/', views.OrderPayView.as_view()),
    path('purchased/list/', views.PurchasedListView.as_view()),
    path('purchased/detail/<int:pk>/', views.PurchasedDetailView.as_view()),
]