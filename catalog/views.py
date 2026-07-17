from django.db.models import Q
from django.shortcuts import get_object_or_404, render

from .models import Category, Product


def product_list(request, category_slug=None):
    categories = Category.objects.all()
    category = None
    products = Product.objects.filter(is_active=True).select_related("category")
    query = request.GET.get("q", "").strip()

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)

    if query:
        products = products.filter(Q(name__icontains=query) | Q(description__icontains=query))

    return render(
        request,
        "catalog/product_list.html",
        {"categories": categories, "category": category, "products": products, "query": query},
    )


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, is_active=True)
    return render(request, "catalog/product_detail.html", {"product": product})

# Create your views here.
