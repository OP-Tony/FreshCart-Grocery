from django.conf import settings
from django.db import models

from catalog.models import Product


class DeliverySlot(models.Model):
    label = models.CharField(max_length=120)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    capacity = models.PositiveIntegerField(default=20)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["date", "start_time"]

    def __str__(self):
        return f"{self.label} - {self.date} ({self.start_time:%I:%M %p}-{self.end_time:%I:%M %p})"


class Order(models.Model):
    PAYMENT_COD = "cod"
    PAYMENT_UPI = "upi"
    PAYMENT_CARD = "card"
    PAYMENT_CHOICES = [
        (PAYMENT_COD, "Cash on Delivery"),
        (PAYMENT_UPI, "UPI"),
        (PAYMENT_CARD, "Card"),
    ]

    STATUS_PLACED = "placed"
    STATUS_CONFIRMED = "confirmed"
    STATUS_PACKED = "packed"
    STATUS_OUT = "out_for_delivery"
    STATUS_DELIVERED = "delivered"
    STATUS_CANCELLED = "cancelled"
    STATUS_CHOICES = [
        (STATUS_PLACED, "Placed"),
        (STATUS_CONFIRMED, "Confirmed"),
        (STATUS_PACKED, "Packed"),
        (STATUS_OUT, "Out for Delivery"),
        (STATUS_DELIVERED, "Delivered"),
        (STATUS_CANCELLED, "Cancelled"),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="orders", on_delete=models.CASCADE)
    delivery_slot = models.ForeignKey(DeliverySlot, on_delete=models.PROTECT)
    delivery_address = models.TextField()
    payment_method = models.CharField(max_length=20, choices=PAYMENT_CHOICES)
    payment_status = models.CharField(max_length=30, default="Simulated")
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default=STATUS_PLACED)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Order #{self.id} by {self.user.username}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    @property
    def line_total(self):
        return self.price * self.quantity

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"

# Create your models here.
