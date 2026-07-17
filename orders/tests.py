from datetime import date, time, timedelta

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from accounts.models import CustomerProfile
from cart.models import CartItem
from catalog.models import Category, Product
from orders.models import DeliverySlot, Order


class CheckoutTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user("buyer", password="pass12345")
        CustomerProfile.objects.create(user=self.user, default_address="Test address")
        category = Category.objects.create(name="Dairy", slug="dairy")
        self.product = Product.objects.create(
            category=category,
            name="Milk",
            slug="milk",
            description="Fresh milk",
            price="60.00",
            stock_quantity=10,
        )
        self.slot = DeliverySlot.objects.create(
            label="Morning",
            date=date.today() + timedelta(days=1),
            start_time=time(8, 0),
            end_time=time(10, 0),
        )

    def test_checkout_creates_order_and_reduces_stock(self):
        CartItem.objects.create(user=self.user, product=self.product, quantity=2)
        self.client.login(username="buyer", password="pass12345")
        response = self.client.post(
            reverse("orders:checkout"),
            {
                "delivery_address": "Test address",
                "delivery_slot": self.slot.id,
                "payment_method": Order.PAYMENT_COD,
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Order.objects.count(), 1)
        self.product.refresh_from_db()
        self.assertEqual(self.product.stock_quantity, 8)
        self.assertFalse(CartItem.objects.filter(user=self.user).exists())
