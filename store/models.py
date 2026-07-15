from django.db import models
from django.contrib.auth.models import User

class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.FloatField()
    description = models.TextField()

    def __str__(self):
        return self.name

class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def total_price(self):
        return self.product.price * self.quantity

class Order(models.Model):
    # خيارات الحالة ووسيلة الدفع عشان تظهر بشكل احترافي في الأدمن
    STATUS_CHOICES = [('Pending', 'Pending'), ('Paid', 'Paid'), ('Shipped', 'Shipped')]
    PAYMENT_METHODS = [('Stripe', 'Stripe/Credit Card'), ('PayPal', 'PayPal'), ('COD', 'Cash on Delivery')]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    total_price = models.FloatField()
    
    # --- الإضافات الجديدة لزوم الـ "بروتوفايلو" ونظام الدفع ---
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS, default='Stripe')
    transaction_id = models.CharField(max_length=100, blank=True, null=True) # رقم العملية اللي بيبهر العميل

    def __str__(self):
        return f"Order {self.id} - {self.user.username}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.CharField(max_length=100)
    price = models.FloatField()
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.quantity} x {self.product}"