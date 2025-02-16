from django.db import models
from book.models import Book  
from customer.models import Customer 
from book.models import Book

class Cart(models.Model):
    id = models.AutoField(primary_key=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="cart_cart")
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="cart_cart")
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.customer.first_name} - {self.book.title} (x{self.quantity})"



