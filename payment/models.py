from django.db import models
from order.models import Order

class Payment(models.Model):
    id = models.AutoField(primary_key=True)
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name="payment_order")
    payment_method = models.CharField(
        max_length=50,
        choices=[
            ("Credit Card", "Credit Card"),
            ("PayPal", "PayPal"),
            ("Bank Transfer", "Bank Transfer"),
        ],
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
