from django.contrib import admin
from .models import Product, CartItem, Order, OrderItem

admin.site.register(Product)
admin.site.register(CartItem)

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    # دي بتخلي شكل المنتجات جوه الطلب في الصورة احترافي جداً
    readonly_fields = ('product', 'price', 'quantity') 

class OrderAdmin(admin.ModelAdmin):
    # زودنا هنا الـ status والـ payment_method والـ transaction_id عشان يظهروا في الجدول الرئيسي
    list_display = ('id', 'user', 'total_price', 'status', 'payment_method', 'transaction_id', 'created_at')
    
    # ضفنا فلاتر على الجنب عشان السكرين شوت تبان إنها "Dashboard" بجد
    list_filter = ('status', 'payment_method', 'created_at')
    
    inlines = [OrderItemInline]

admin.site.register(Order, OrderAdmin)