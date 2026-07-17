from datetime import date, time, timedelta
from decimal import Decimal

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.utils.text import slugify

from accounts.models import CustomerProfile
from catalog.models import Category, Product
from orders.models import DeliverySlot


class Command(BaseCommand):
    help = "Create demo grocery categories, products, delivery slots, and users."

    def handle(self, *args, **options):
        categories = {
            "Fruits": "Fresh seasonal fruits for daily nutrition.",
            "Vegetables": "Farm-fresh vegetables and greens.",
            "Dairy": "Milk, curd, paneer, butter, and cheese.",
            "Grains": "Rice, wheat, pulses, and staples.",
            "Bakery": "Bread, buns, biscuits, and breakfast items.",
            "Beverages": "Tea, coffee, juices, and soft drinks.",
            "Household": "Everyday cleaning and home essentials.",
        }

        category_objs = {}
        for name, description in categories.items():
            category_objs[name], _ = Category.objects.update_or_create(
                slug=slugify(name),
                defaults={"name": name, "description": description},
            )

        products = [
            ("Fruits", "Banana", "Fresh yellow bananas, perfect for snacks and smoothies.", "48.00", 80),
            ("Fruits", "Apple", "Crisp red apples sourced from trusted orchards.", "160.00", 55),
            ("Fruits", "Orange", "Juicy oranges rich in vitamin C.", "110.00", 65),
            ("Fruits", "Grapes", "Seedless green grapes packed hygienically.", "95.00", 40),
            ("Fruits", "Watermelon", "Large sweet watermelon for family servings.", "70.00", 25),
            ("Vegetables", "Tomato", "Fresh red tomatoes for curries and salads.", "38.00", 90),
            ("Vegetables", "Potato", "Clean potatoes suitable for everyday cooking.", "32.00", 120),
            ("Vegetables", "Onion", "Medium-size onions for Indian kitchens.", "42.00", 100),
            ("Vegetables", "Carrot", "Crunchy carrots for salads and cooking.", "58.00", 60),
            ("Vegetables", "Spinach", "Fresh spinach bunches cleaned and sorted.", "25.00", 45),
            ("Dairy", "Milk 1L", "Toned milk pouch for daily household use.", "62.00", 70),
            ("Dairy", "Curd 500g", "Thick and creamy curd cup.", "45.00", 60),
            ("Dairy", "Paneer 200g", "Soft paneer for curries and snacks.", "95.00", 35),
            ("Dairy", "Butter 100g", "Salted table butter.", "58.00", 40),
            ("Dairy", "Cheese Slices", "Processed cheese slices for sandwiches.", "125.00", 32),
            ("Grains", "Basmati Rice 1kg", "Long-grain basmati rice.", "145.00", 50),
            ("Grains", "Wheat Flour 5kg", "Whole wheat atta for chapatis.", "260.00", 45),
            ("Grains", "Toor Dal 1kg", "Premium toor dal for everyday cooking.", "165.00", 40),
            ("Grains", "Chana Dal 1kg", "High-protein chana dal.", "120.00", 42),
            ("Grains", "Sugar 1kg", "Refined sugar for kitchen use.", "48.00", 75),
            ("Bakery", "Brown Bread", "Fresh brown bread loaf.", "55.00", 35),
            ("Bakery", "White Bread", "Soft white sandwich bread.", "45.00", 38),
            ("Bakery", "Burger Buns", "Pack of soft burger buns.", "60.00", 28),
            ("Bakery", "Jeera Biscuits", "Crisp cumin biscuits.", "35.00", 50),
            ("Bakery", "Rusk Pack", "Tea-time rusk pack.", "40.00", 45),
            ("Beverages", "Tea Powder 250g", "Strong tea powder blend.", "140.00", 36),
            ("Beverages", "Instant Coffee 100g", "Rich instant coffee powder.", "190.00", 30),
            ("Beverages", "Mango Juice 1L", "Ready-to-serve mango juice.", "95.00", 44),
            ("Beverages", "Lemon Soda", "Refreshing lemon soda bottle.", "35.00", 60),
            ("Beverages", "Mineral Water 1L", "Packaged drinking water.", "20.00", 100),
            ("Household", "Dishwash Liquid", "Lemon fragrance dishwash liquid.", "115.00", 34),
            ("Household", "Floor Cleaner", "Disinfectant floor cleaner.", "175.00", 26),
            ("Household", "Laundry Detergent", "Powder detergent for daily laundry.", "220.00", 28),
            ("Household", "Tissue Roll", "Soft tissue roll pack.", "85.00", 40),
            ("Household", "Garbage Bags", "Medium garbage bags roll.", "110.00", 30),
        ]

        for category_name, name, description, price, stock in products:
            Product.objects.update_or_create(
                slug=slugify(name),
                defaults={
                    "category": category_objs[category_name],
                    "name": name,
                    "description": description,
                    "price": Decimal(price),
                    "stock_quantity": stock,
                    "is_active": True,
                },
            )

        today = date.today()
        slot_specs = [
            ("Morning", time(8, 0), time(10, 0)),
            ("Late Morning", time(10, 0), time(12, 0)),
            ("Afternoon", time(14, 0), time(16, 0)),
            ("Evening", time(18, 0), time(20, 0)),
        ]
        for day_offset in range(1, 4):
            slot_date = today + timedelta(days=day_offset)
            for label, start, end in slot_specs:
                DeliverySlot.objects.update_or_create(
                    label=label,
                    date=slot_date,
                    start_time=start,
                    defaults={"end_time": end, "capacity": 20, "is_active": True},
                )

        admin, created = User.objects.get_or_create(
            username="admin",
            defaults={"email": "admin@example.com", "is_staff": True, "is_superuser": True},
        )
        if created:
            admin.set_password("admin123")
            admin.save()

        customer, created = User.objects.get_or_create(
            username="customer",
            defaults={"email": "customer@example.com", "first_name": "Demo", "last_name": "Customer"},
        )
        if created:
            customer.set_password("customer123")
            customer.save()
        CustomerProfile.objects.update_or_create(
            user=customer,
            defaults={
                "phone": "9999999999",
                "default_address": "Demo House, College Road, Hyderabad",
            },
        )

        self.stdout.write(self.style.SUCCESS("Demo data created. Admin: admin/admin123, Customer: customer/customer123"))
