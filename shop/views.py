from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth import authenticate
from django.contrib import messages
from shop.forms import OrderForm, PaymentForm, ContactForm, NewsletterForm
from .decorators import redirect_authenticated_user, login_required_user
from .models import Order, OrderItem, Product, Cart, CartItem, Category,Wishlist,WishlistItem, Review, Payment, NewsletterSubscription
from django.http import JsonResponse
from django.db.models import Q
from django.http import JsonResponse
import json
# Create your views here.
def search(request):
    query = request.GET.get('q')
    if query:
        products = Product.objects.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query)
        )
    else:
        products = Product.objects.none()
    
    return render(request, 'shop/search_results.html', {'products': products, 'query': query})


@login_required_user
def my_orders(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'shop/my_orders.html', {'orders': orders})


@login_required_user
def order_detail(request, order_id):
    order = get_object_or_404(Order, order_id=order_id)
    if order.user != request.user:
        messages.error(request, "You do not have permission to view this order.")
        return redirect('index')
    
    order_items = []
    total_price = 0
    for item in order.items.all():
        item_total = item.product.price * item.quantity
        order_items.append({
            'product': item.product,
            'quantity': item.quantity,
            'price': item.product.price,
            'total': item_total
        })
        total_price += item_total
    
    context = {
        'order': order,
        'order_items': order_items,
        'total_price': total_price
    }
    
    return render(request, 'shop/order_detail.html', context)

@login_required_user
def add_review(request, product_id):
    product = get_object_or_404(Product, product_id=product_id)
    if request.method == 'POST':
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')
        existing_review = Review.objects.filter(product=product, user=request.user).first()
        if existing_review:
            messages.error(request, "You have already submitted a review for this product.")
        else:
            review = Review.objects.create(
                product=product,
                user=request.user,
                rating=rating,
                comment=comment
            )
            messages.success(request, "Review submitted successfully.")
    return redirect('product_detail', product_id=product_id)

@login_required_user
def delete_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    if request.user == review.user:
        review.delete()
        messages.success(request, "Your review has been deleted.")
    else:
        messages.error(request, "You cannot delete this review.")
    return redirect('product_detail', product_id=review.product.product_id)
#index view
def index(request):
    categories = Category.objects.all()
    return render(request, 'shop/index.html', {'categories': categories})

def subscribe_newsletter(request):
    if request.method == 'POST':
        form = NewsletterForm(request.POST)
        email = request.POST.get('email')  # Extract email from POST data
        if email and NewsletterSubscription.objects.filter(email=email).exists():
            messages.warning(request, 'You are already subscribed.')
        elif form.is_valid():
            form.save()
            messages.success(request, 'Successfully subscribed to the newsletter.')
        else:
            messages.error(request, 'Invalid email address.')
    return redirect('index')

def category_view(request, category_name):
    category = get_object_or_404(Category, name__iexact=category_name)
    products = Product.objects.filter(category=category)
    context = {
        'category': category,
        'products': products,
    }
    return render(request, 'shop/category.html', context)

def product_detail(request, product_id):
    product = get_object_or_404(Product, product_id=product_id)
    return render(request, 'shop/product.html', {'product': product})


@redirect_authenticated_user
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            auth_login(request, user)
            return redirect('index')
    else:
        form = UserCreationForm()
    return render(request, 'shop/register.html', {'form': form})
#create a login view using shop/login.html template
@redirect_authenticated_user
def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect('index')  
    else:
        form = AuthenticationForm()
    return render(request, 'shop/login.html', {'form': form})
#create logout 
@login_required_user
def logout(request):
    auth_logout(request)
    return redirect('login')

@login_required_user
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, product_id=product_id)
    cart, _ = Cart.objects.get_or_create(user=request.user)

    if product.quantity > 0:
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        if created:
            cart_item.quantity = 1
            messages.success(request, f"Added {product.name} to your cart.")
        else:
            if cart_item.quantity < product.quantity:
                cart_item.quantity += 1
                messages.success(request, f"Updated quantity for {product.name}.")
            else:
                messages.error(request, f"Cannot add more {product.name}. Only {product.quantity} in stock.")
                return redirect('cart')
        cart_item.save()
    else:
        messages.error(request, f"{product.name} is out of stock.")
        return redirect('cart')
    
    return redirect('cart')
    
@login_required_user
def cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.items.all()
    for item in cart_items:
        item.total_price = item.product.price * item.quantity

    total_price = sum(item.total_price for item in cart_items)
    return render(request, 'shop/cart.html', {
        'cart': cart,
        'cart_items': cart_items,
        'total_price': total_price
    })
@login_required_user
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    cart_item.delete()
    return redirect('cart')

@login_required_user
def clear_cart(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    cart.clear()
    return redirect('cart')
    
@login_required_user
def checkout(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.items.all()
    for item in cart_items:
        item.total_price = item.product.price * item.quantity

    total_price = sum(item.total_price for item in cart_items)

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.status = 'processing'
            order.save()

            for item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity
                )
                item.product.quantity -= item.quantity
                item.product.save()

            cart.clear()

            payment_method = request.POST.get('payment_method')
            if payment_method == 'cod':
                Payment.objects.create(order=order, method='cod')
                return redirect('order_success', order_id=order.order_id)
            else:
                return redirect('payment', order_id=order.order_id)
    else:
        form = OrderForm()

    return render(request, 'shop/checkout.html', {
        'cart': cart,
        'cart_items': cart_items,
        'total_price': total_price,
        'form': form
    })

@login_required_user
def payment(request, order_id):
    order = get_object_or_404(Order, order_id=order_id)
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.order = order
            payment.method = 'card'
            payment.save()
            return redirect('order_success', order_id=order.order_id)
    else:
        form = PaymentForm()

    return render(request, 'shop/payment.html', {
        'order': order,
        'form': form
    })

@login_required_user
def order_success(request, order_id):
    if request.user != Order.objects.get(order_id=order_id).user:
        return redirect('index')
    order = get_object_or_404(Order, order_id=order_id)
    return render(request, 'shop/order_success.html', {'order': order})

@login_required_user
def wishlist(request):
    wishlist, _ = Wishlist.objects.get_or_create(user=request.user)
    wishlist_items = wishlist.products.all()
    return render(request, 'shop/wishlist.html', {'wishlist_items': wishlist_items})

@login_required_user
def add_to_wishlist(request, product_id):
    product = get_object_or_404(Product, product_id=product_id)
    wishlist, _ = Wishlist.objects.get_or_create(user=request.user)
    WishlistItem.objects.get_or_create(wishlist=wishlist, product=product)
    return redirect('wishlist')

@login_required_user
def remove_from_wishlist(request, product_id):
    product = get_object_or_404(Product, product_id=product_id)
    wishlist = get_object_or_404(Wishlist, user=request.user)
    wishlist_item = get_object_or_404(WishlistItem, wishlist=wishlist, product=product)
    wishlist_item.delete()
    return redirect('wishlist')

def about_us(request):
    return render(request, 'shop/about_us.html')

def faq(request):
    return render(request, 'shop/faq.html')

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your message has been sent successfully.')
            return redirect('contact')
    else:
        form = ContactForm()
    return render(request, 'shop/contact.html', {'form': form})

@login_required_user
def update_cart_item_quantity(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            item_id = data.get('item_id')
            change = data.get('change')

            if item_id is None or change is None:
                messages.error(request, 'Invalid data provided')
                return JsonResponse({'status': 'error'}, status=400)

            change = int(change)
            
            cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
            
            if change == -1 and cart_item.quantity > 1:
                cart_item.quantity -= 1
                messages.success(request, f'Updated quantity for {cart_item.product.name}.')
            elif change == 1 and cart_item.quantity < cart_item.product.quantity:
                cart_item.quantity += 1
                messages.success(request, f'Updated quantity for {cart_item.product.name}.')
            elif change == -1 and cart_item.quantity == 1:
                messages.error(request, 'Quantity cannot be less than 1.')
            else:
                messages.error(request, f'Cannot add more {cart_item.product.name}. Only {cart_item.product.quantity} in stock.')
                return JsonResponse({'status': 'error'})
            
            cart_item.save()
            return JsonResponse({'status': 'success'})
        except (ValueError, KeyError, json.JSONDecodeError) as e:
            messages.error(request, 'Invalid request')
            return JsonResponse({'status': 'error'}, status=400)
    messages.error(request, 'Invalid request method')
    return JsonResponse({'status': 'error'}, status=400)

@login_required_user
def cancel_order(request, order_id):
    order = get_object_or_404(Order, order_id=order_id, user=request.user)
    if order.status == 'processing':
        order.status = 'cancelled'
        order.save()
        messages.success(request, f"Order {order.order_id} has been cancelled.")
    else:
        messages.error(request, "This order cannot be cancelled.")
    return redirect('order_detail', order_id=order_id)