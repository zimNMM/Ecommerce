from django.contrib import admin
from .models import Category, Product, Cart, CartItem, Order, OrderItem

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'quantity', 'available')
    list_filter = ('available', 'category')
    search_fields = ('name', 'category__name')
    list_editable = ('price', 'quantity', 'available')

class CartItemInline(admin.TabularInline):
    model = CartItem
    raw_id_fields = ('product',)

class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at')
    search_fields = ('user__username',)
    inlines = [CartItemInline]

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ('product',)

class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'user', 'fullname', 'address', 'status', 'created_at', 'tracking_id')
    list_filter = ('status', 'created_at')
    search_fields = ('order_id', 'user__username', 'fullname')
    inlines = [OrderItemInline]
    readonly_fields = ('order_id', 'created_at')

admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Cart, CartAdmin)
admin.site.register(Order, OrderAdmin)
