from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render

from accounts.models import CustomerProfile
from cart.models import CartItem

from .forms import CheckoutForm
from .models import Order, OrderItem


@login_required
def checkout(request):
    cart_items = list(CartItem.objects.filter(user=request.user).select_related("product"))
    if not cart_items:
        messages.warning(request, "Your cart is empty.")
        return redirect("cart:detail")

    for item in cart_items:
        if item.quantity > item.product.stock_quantity:
            messages.error(request, f"Only {item.product.stock_quantity} units of {item.product.name} are available.")
            return redirect("cart:detail")

    profile, _ = CustomerProfile.objects.get_or_create(
        user=request.user, defaults={"default_address": ""}
    )
    initial = {"delivery_address": profile.default_address}

    if request.method == "POST":
        form = CheckoutForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                total = sum(item.line_total for item in cart_items)
                order = form.save(commit=False)
                order.user = request.user
                order.total_amount = total
                order.save()

                for item in cart_items:
                    product = item.product
                    if item.quantity > product.stock_quantity:
                        raise ValueError("Stock changed while checking out.")
                    OrderItem.objects.create(
                        order=order,
                        product=product,
                        quantity=item.quantity,
                        price=product.price,
                    )
                    product.stock_quantity -= item.quantity
                    product.save(update_fields=["stock_quantity"])
                CartItem.objects.filter(user=request.user).delete()
            messages.success(request, "Order placed successfully.")
            return redirect("orders:success", order_id=order.id)
    else:
        form = CheckoutForm(initial=initial)

    total = sum(item.line_total for item in cart_items)
    return render(request, "orders/checkout.html", {"form": form, "items": cart_items, "total": total})


@login_required
def order_success(request, order_id):
    order = get_object_or_404(Order.objects.prefetch_related("items__product"), id=order_id, user=request.user)
    return render(request, "orders/success.html", {"order": order})


@login_required
def my_orders(request):
    orders = Order.objects.filter(user=request.user).prefetch_related("items__product")
    return render(request, "orders/my_orders.html", {"orders": orders})

# Create your views here.
