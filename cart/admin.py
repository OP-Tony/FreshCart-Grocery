from django.contrib import admin

from .models import CartItem


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ("user", "product", "quantity", "line_total", "updated_at")
    list_filter = ("updated_at",)
    search_fields = ("user__username", "product__name")

# Register your models here.
