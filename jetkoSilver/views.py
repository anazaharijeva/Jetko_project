from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from .forms import CheckoutForm, ItemForm


def jewellery(request):
    query = request.GET.get('search_query', '')
    jewelry_type = request.GET.getlist('jewelry_type')
    material = request.GET.getlist('material')
    color = request.GET.getlist('color')
    all_jewelries = Product.objects.all()

    if query:
        all_jewelries = all_jewelries.filter(jewelry_type_icontains=query)

    if jewelry_type:
        all_jewelries = all_jewelries.filter(jewelry_type__in=jewelry_type)

    if material:
        all_jewelries = all_jewelries.filter(material__in=material)

    if color:
        all_jewelries = all_jewelries.filter(color__in=color)

    return render(request, 'jewellery.html',
                  {'jewellery': all_jewelries, 'query': query, 'selected_jewelry_type': jewelry_type,
                   'selected_material': material,
                   'selected_color': color, 'user': request.user})


@login_required(login_url='login')
def jewellery_details(request, jewellery_id):
    jewellery = get_object_or_404(Product, id=jewellery_id)
    cart, created = Cart.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        # Check if the purchased quantity is available
        if quantity <= jewellery.quantity:
            cart_item, created = CartItem.objects.get_or_create(cart=cart, product=jewellery)
            cart_item.quantity = quantity
            cart_item.save()
            return redirect('cart_items')
        else:
            return HttpResponse("Insufficient quantity available")
    return render(request, 'jewellery_details.html', {'jewellery': jewellery})


@login_required
def delete_item(request, item_id):
    item = get_object_or_404(Product, id=item_id)
    item.delete()
    return redirect('jewellery')


@login_required
def edit_item(request, item_id):
    item = get_object_or_404(Product, id=item_id)
    if request.method == 'POST':
        form = ItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect('jewellery_details', jewellery_id=item.id)
    else:
        form = ItemForm(instance=item)
    return render(request, 'edit_product.html', {'form': form, 'item': item})


@login_required
def add_item(request):
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('jewellery_details',
                            jewellery_id=form.save().id)  # Redirect to the cart or any other appropriate URL
    else:
        form = ItemForm()
    return render(request, 'add_product.html', {'form': form})


@login_required(login_url='login')
def cart_items(request):
    items = CartItem.objects.filter(cart__user=request.user)
    cart_total = sum(item.product.price * item.quantity for item in items)
    context = {'cart_items': items, 'total': cart_total}
    return render(request, 'cart_items.html', context)


@login_required
def delete_cart_item(request, item_id):
    item = get_object_or_404(CartItem, id=item_id)
    item.delete()
    return redirect('cart_items')


@login_required(login_url='login')
def checkout(request):
    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.cart = request.user.cart  # Assuming you have associated each user with a cart
            order.total_amount = order.calculate_total_amount()  # Calculate the total amount
            order.save()
            # Subtract the purchased quantities from the products' quantities
            items = order.cart.items.all()
            for cart_item in items:
                cart_item.product.quantity -= cart_item.quantity
                cart_item.product.save()
            # Clear the cart items
            request.user.cart.items.all().delete()
            # Redirect or render success page
            return redirect('final_site')
        # else:
        #     return redirect('cases')
    else:
        form = CheckoutForm()
    context = {'form': form}
    return render(request, 'checkout.html', context)


@login_required(login_url='login')
def final_site(request):
    return render(request, 'final_site.html')


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('jewellery')
        else:
            # Handle invalid login credentials
            return render(request, 'login.html', {'error': 'Invalid login credentials.'})
    return render(request, 'login.html')
