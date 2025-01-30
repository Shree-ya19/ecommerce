from django.shortcuts import render,HttpResponse,redirect
from django.http import JsonResponse
import json
import datetime
from .models import *
from .utils import cookieCart, cartData, guestOrder
from django.contrib.auth.models import User,auth
from .models import Customer
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User,auth
from django.contrib.auth.forms import UserCreationForm
from.forms import CreateUserForm
from django import forms
from django.contrib import messages
from .models import Product
from django.db.models import Q


def home(request):
    return render(request,'store/home.html')


def store(request):
    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    products = Product.objects.all()
    context = {'products': products, 'cartItems': cartItems}
    return render(request, 'store/store.html', context)




def cart(request):
    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'store/cart.html', context)


def checkout(request):
    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'store/checkout.html', context)


def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print('Action:', action)
    print('Product:', productId)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)


def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
    else:
        customer, order = guestOrder(request, data)

    total = float(data['form']['total'])
    order.transaction_id = transaction_id

    if total == order.get_cart_total:
        order.complete = True
    order.save()

    if order.shipping == True:
        ShippingAddress.objects.create(
            customer=customer,
            order=order,
            address=data['shipping']['address'],
            city=data['shipping']['city'],
            state=data['shipping']['state'],
            zipcode=data['shipping']['zipcode'],
        )

    return JsonResponse('Payment submitted..', safe=False)



def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            # *Check if user has a customer, if not, create one*
            if not hasattr(user, 'customer'):
                Customer.objects.create(user=user, name=user.username, email=user.email)

            messages.success(request, 'You have logged in successfully')
            return redirect('store')  # Adjust redirect as needed
        else:
            messages.error(request, 'Sorry! There was an error. Try Again')
            return redirect('login')

    return render(request, 'store/login.html')


def logout_user(request):
    logout(request)
    messages.success(request,' You have logged out...Thank you for visit')
    return redirect('store')


def signup_user(request):
    form = CreateUserForm()

    if request.method=='POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user=form.cleaned_data.get('username')
            messages.success(request,'Account was created for ' + user)
            return redirect('login')



    return render(request,'store/signup.html',{'form': form})



def search(request):
    # Get the data for the cart
    data = cartData(request)

    # Get the number of items in the cart
    cartItems = data['cartItems']

    query = request.POST.get('searched', '').lower()  # Get the search query and make it case-insensitive
    products = Product.objects.all()  # Get all products from the database

    if query:
        # Initialize an empty list to store search results
        searched = []

        # Apply linear search by iterating through all products
        for product in products:
            if query in product.name.lower():  # Check if the search term is in the product name (case-insensitive)
                searched.append(product)
    else:
        searched = products  # If no search term is entered, show all products

    # Pass `cartItems` and `searched` to the template
    return render(request, 'store/search.html', {'searched': searched, 'cartItems': cartItems})
