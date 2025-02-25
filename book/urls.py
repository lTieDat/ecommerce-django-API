from django.urls import path
from .views import BookAPIView

urlpatterns = [
    path('books/', BookAPIView.as_view(), name='book_home'),
    path('books/<int:book_id>/', BookAPIView.as_view(), name='book_detail'),
]