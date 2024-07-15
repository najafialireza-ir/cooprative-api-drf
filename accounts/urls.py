from django.urls import path
from . import views


urlpatterns = [
    path('user/register/', views.UserRegisterView.as_view()),
    path('user/profile/', views.UserProfileView.as_view({'get': 'list', 'patch': 'partial_update'})),
]

# {'get': 'retrieve', 'patch': 'partial_update'}