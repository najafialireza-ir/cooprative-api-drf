from django.urls import path
from . import views


urlpatterns = [
    path('car/choice/user/', views.DriverCarCreateView.as_view()),
    path('car/', views.CarRegisterListView.as_view()),
    path('car/detail/<int:pk>/', views.CarDetailView.as_view({'get':'retrieve', 'patch': 'partial_update','delete': 'destroy'})),
    
    
    path('baseprice/travel/', views.BasePriceView.as_view()),
    path('basetime/travel/', views.BaseTimeView.as_view()),
    
    path('driver/detail/', views.DriverDetailView.as_view({
        'patch': 'partial_update', 'delete': 'destroy'})),
    
    path('driver/list', views.DriverListView.as_view()),
    path('city/', views.CityCreateOrListView.as_view()),
    path('city/detail/<int:pk>/', views.CityDetailView.as_view({'get':'retrieve', 'patch': 'partial_update','delete': 'destroy'})),
    
]

