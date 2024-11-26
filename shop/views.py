from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Product, Order, UserProfile
from django.http import HttpResponse
import stripe
from django.conf import settings
from decimal import Decimal
from .models import Card,Carts
from .forms import CardForm



from django.http import JsonResponse


#stripe.api_key = 'your-stripe-secret-key'



def index(request):
   
    return render(request, 'shop/index.html')

# Product listing page
def product_list(request):
    products = Product.objects.all()
    
    
    return render(request, 'shop/product_list.html', {
        'products': products,
        })

# Product detail page
def product_detail(request, product_id):
    products = Product.objects.get(id=product_id)
    print(products)
    return render(request, 'shop/product_detail.html', {'products': products})

# Add to cart


def card_view(request):
    cards = Carts.objects.filter(user=request.user)
    total_price = sum([card.Products.price * card.quantity for card in cards])
    
    return render(request, 'shop/cards.html', {'cards': cards , 'total_price': total_price})

def add_card(request,id):
    quantity=1
    p=Carts.objects.create(user=request.user, Products=Product.objects.get(id=id), quantity=quantity)
    
    print(p.Products)
    return redirect('card_view')
    #if request.method == 'POST':
     #   form = CardForm(request.POST)
      #  if form.is_valid():
         #   form.save()
           # return redirect('card_view')
    #else:
        #form = CardForm()
    #return render(request, 'add_card.html', {'form': form})


# remove Cart
def remove_cart_item(request, cart_item_id):
    # Get the cart item to remove
    cart_item = get_object_or_404(Carts, id=cart_item_id, user=request.user)
    
    # Remove the item from the cart
    cart_item.delete()
    
    # Redirect the user back to the cart view
    return redirect('card_view')

def update_cart_quantity(request, cart_item_id):
    # Ensure the method is POST
    if request.method == 'POST':
        # Get the cart item object for the current user
        cart_item = get_object_or_404(Carts, id=cart_item_id, user=request.user)

        # Get the action (whether to increase or decrease the quantity)
        action = request.POST.get('action')

        if action == 'increase':
            # Increase the quantity of the product
            cart_item.quantity += 1
            cart_item.save()

        elif action == 'decrease':
            # Decrease the quantity (ensure quantity does not go below 1)
            if cart_item.quantity > 1:
                cart_item.quantity -= 1
                cart_item.save()

        # Redirect back to the cart view after the update
        return redirect('card_view')

    # If not POST, fallback to the cart view
    return render(request, 'cart.html')

def cart_view(request):
    cards = Carts.objects.filter(user=request.user)
    total_price = sum([card.Products.price * card.quantity for card in cards])
    print(cards)
    return render(request, 'cart.html', {'cards': cards, 'total_price': total_price})

# User registration and login
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
    else:
        form = UserCreationForm()
    return render(request, 'shop/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('index')
    else:
        form = AuthenticationForm()
    return render(request, 'shop/login.html', {'form': form})
def payment_page(request):
    cards = Carts.objects.filter(user=request.user)
    total_price = sum([card.Products.price * card.quantity for card in cards])
    
    return render(request, 'shop/payment.html',{'cards': cards,'total_price':total_price})

# Process the payment (Cash on Delivery)
def process_cod_payment(request):
    if request.method == 'POST':
        payment_method = request.POST.get('payment_method')
        
        if payment_method == 'cash_on_delivery':
            # Here you can save the order to the database, mark it as pending payment, etc.
            # For simplicity, we are just passing the payment method to the confirmation page.
            return render(request, 'shop/payment_successful.html', {'payment_method': 'Cash on Delivery'})
        
        return HttpResponse("Invalid Payment Method", status=400)
    return HttpResponse("Invalid Request", status=400)
