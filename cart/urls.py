from django.urls import path
from .views import CartAPIView

urlpatterns = [
    path('cart/all', CartAPIView.as_view(), name='cart-list'),  # Handles GET (all carts) and POST
    path('cart/<str:customer_name>/', CartAPIView.as_view(), name='cart-detail'),  # Handles GET for a specific customer
    path('cart/<int:cart_id>/', CartAPIView.as_view(), name='cart-update-delete'),  # Handles PUT and DELETE
]
