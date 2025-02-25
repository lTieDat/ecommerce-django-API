from django.urls import path
from .views import CartAPIView

urlpatterns = [
    path('cart/all', CartAPIView.as_view(), name='cart-list'), 
    path('cart/<str:email>/', CartAPIView.as_view(), name='cart-detail'), 
    path('cart/<int:cart_id>/', CartAPIView.as_view(), name='cart-update-delete'),  
]
