from django.contrib import admin

from .models import DeliverySlot, Order, OrderItem


@admin.register(DeliverySlot)
class DeliverySlotAdmin(admin.ModelAdmin):
    list_display = ("label", "date", "start_time", "end_time", "capacity", "is_active")
    list_filter = ("date", "is_active")
    list_editable = ("capacity", "is_active")


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ("product", "quantity", "price", "line_total")


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "total_amount", "payment_method", "status", "created_at")
    list_filter = ("status", "payment_method", "created_at")
    list_editable = ("status",)
    search_fields = ("user__username", "delivery_address")
    inlines = [OrderItemInline]

# Register your models here.
