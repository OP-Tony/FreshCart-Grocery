from django.test import TestCase
from django.urls import reverse

from catalog.models import Category, Product


class CatalogTests(TestCase):
    def test_product_search(self):
        category = Category.objects.create(name="Fruits", slug="fruits")
        Product.objects.create(
            category=category,
            name="Banana",
            slug="banana",
            description="Fresh banana",
            price="45.00",
            stock_quantity=10,
        )
        response = self.client.get(reverse("catalog:product_list"), {"q": "banana"})
        self.assertContains(response, "Banana")
