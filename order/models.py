from django.db import models
from cart.models import Cart

class Order(models.Model):
    id = models.AutoField(primary_key=True)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="order_cart")
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=50,
        choices=[
            ("Pending", "Pending"),
            ("Confirmed", "Confirmed"),
            ("Shipped", "Shipped"),
            ("Delivered", "Delivered"),
        ],
        default="Pending",
    )

    def __str__(self):
        return f"Order {self.id}"

