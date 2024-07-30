import random
from django.contrib import admin
from shop.models import Category, Product, Cart, CartItem, Order, OrderItem, Wishlist, WishlistItem, Review, Payment,Contact,NewsletterSubscription

class PaymentAdmin(admin.ModelAdmin):
    list_display = ('order', 'method', 'card_number', 'card_expiry_date', 'card_cvc')
    search_fields = ('order__order_id', 'method')


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)
    list_display_links = ('name',)
    fields = ('name', 'description', 'image')
    
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

class NewsletterSubscriptionAdmin(admin.ModelAdmin):
    list_display = ('email',)
    search_fields = ('email',)

def generate_tracking_id():
    return ''.join([str(random.randint(0, 9)) for _ in range(10)])

def mark_as_shipped(modeladmin, request, queryset):
    for order in queryset:
        if order.status == 'processing':
            order.tracking_id = generate_tracking_id()
            order.status = 'shipped'
            order.save()

mark_as_shipped.short_description = "Generate tracking ID and mark as shipped (only for processing orders)"

class StatusFilter(admin.SimpleListFilter):
    title = 'Status'
    parameter_name = 'status'

    def lookups(self, request, model_admin):
        return (
            ('all', 'All'),
            ('processing', 'Processing'),
            ('shipped', 'Shipped'),
            ('delivered', 'Delivered'),
            ('cancelled', 'Cancelled'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'processing':
            return queryset.filter(status='processing')
        elif self.value() == 'shipped':
            return queryset.filter(status='shipped')
        elif self.value() == 'delivered':
            return queryset.filter(status='delivered')
        elif self.value() == 'cancelled':
            return queryset.filter(status='cancelled')
        return queryset

class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'user', 'fullname', 'address', 'status', 'created_at', 'tracking_id')
    list_filter = ('status', StatusFilter, 'created_at')
    search_fields = ('order_id', 'user__username', 'fullname')
    inlines = [OrderItemInline]
    readonly_fields = ('order_id', 'created_at')
    actions = [mark_as_shipped]

class WishlistItemInline(admin.TabularInline):
    model = WishlistItem
    raw_id_fields = ('product',)

class WishlistAdmin(admin.ModelAdmin):
    list_display = ('user',)
    search_fields = ('user__username',)
    inlines = [WishlistItemInline]

class ReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'rating', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__username', 'product__name')

class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'created_at')
    search_fields = ('name', 'email')
admin.site.register(NewsletterSubscription, NewsletterSubscriptionAdmin)
admin.site.register(Contact, ContactAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Cart, CartAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Wishlist, WishlistAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Payment, PaymentAdmin)
