from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Product, CartItem, Order, OrderItem


def home(request):
    products = Product.objects.all()
    return render(request, "store/home.html", {"products": products})


def add_to_cart(request, product_id):
    cart_item, created = CartItem.objects.get_or_create(
        user=request.user,
        product_id=product_id
    )

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('home')


@login_required
def checkout(request):
    cart_items = CartItem.objects.filter(user=request.user)

    if not cart_items:
        return redirect('home')

    total = 0
    for item in cart_items:
        total += item.total_price()

    order = Order.objects.create(
        user=request.user,
        total_price=total
    )

    for item in cart_items:
        OrderItem.objects.create(
            order=order,
            product=item.product.name,
            price=item.product.price,
            quantity=item.quantity
        )

    cart_items.delete()

    return render(request, "store/checkout_success.html", {"order": order})