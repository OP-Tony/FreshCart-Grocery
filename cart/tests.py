from django.contrib.auth.models import User
from django.test import TestCase

from catalog.models import Category, Product
from cart.models import CartItem


class CartTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user("buyer", password="pass12345")
        category = Category.objects.create(name="Fruits", slug="fruits")
        self.product = Product.objects.create(
            category=category,
            name="Apple",
            slug="apple",
            description="Fresh apples",
            price="100.00",
            stock_quantity=5,
        )

    def test_cart_line_total(self):
        item = CartItem.objects.create(user=self.user, product=self.product, quantity=3)
        self.assertEqual(item.line_total, self.product.price * 3)
