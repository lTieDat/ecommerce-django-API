from django.urls import path
from .views import CustomerAPIView
from rest_framework_simplejwt import views as jwt_views

urlpatterns = [
    path('customers/', CustomerAPIView.as_view(), name='customer_list'),  # GET all, POST new
    path('customers/<int:customer_id>/', CustomerAPIView.as_view(), name='customer_detail'),  # GET, PUT, DELETE by ID
]
