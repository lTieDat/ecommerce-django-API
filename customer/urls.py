from django.urls import path
from .views import CustomerAPIView


urlpatterns = [
    path('customers/', CustomerAPIView.as_view(), name='customer_list'),  
    path('customers/<str:customer_username>/', CustomerAPIView.as_view(), name='customer_detail'), 
]
