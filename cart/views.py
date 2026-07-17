from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from catalog.models import Product

from .models import CartItem


@login_required
def cart_detail(request):
    items = CartItem.objects.filter(user=request.user).select_related("product")
    total = sum(item.line_total for item in items)
    return render(request, "cart/detail.html", {"items": items, "total": total})


@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id, is_active=True)
    if not product.in_stock:
        messages.error(request, "This product is currently out of stock.")
        return redirect(product.get_absolute_url())

    quantity = max(1, int(request.POST.get("quantity", 1)))
    item, _ = CartItem.objects.get_or_create(user=request.user, product=product)
    item.quantity = min(item.quantity + quantity, product.stock_quantity)
    item.save()
    messages.success(request, f"{product.name} added to cart.")
    return redirect("cart:detail")


@login_required
def update_cart_item(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, user=request.user)
    quantity = max(1, int(request.POST.get("quantity", 1)))
    if quantity > item.product.stock_quantity:
        messages.warning(request, f"Only {item.product.stock_quantity} units are available.")
    item.quantity = min(quantity, item.product.stock_quantity)
    item.save()
    return redirect("cart:detail")


@login_required
def remove_cart_item(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, user=request.user)
    item.delete()
    messages.info(request, "Item removed from cart.")
    return redirect("cart:detail")

# Create your views here.
