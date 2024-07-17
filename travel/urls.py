from django.urls import path
from . import views


urlpatterns = [
    path('', views.TravelListOrCreateView.as_view({'get': 'list', 'post': 'create'})),
    path('ticket/list/<int:pk>/', views.TicketListView.as_view()),
    path('detail/<int:pk>/', views.TravelDetailView.as_view({'get':'retrieve', 'patch': 'partial_update','delete': 'destroy'})),
    
    path('update/accept/<int:pk>/', views.TravelUpdateView.as_view({'patch': 'partial_update', 'delete': 'destroy'})),
    path('request/list/', views.TravelRequestListView.as_view()),
    path('expert/excel/', views.TravelExportExcel.as_view()),
    
]