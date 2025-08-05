from django.shortcuts import render
from .models import Product
from django.contrib.auth.decorators import login_required
from .forms import PrescriptionForm
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Order, OrderItem, Prescription, UserProfile
from .forms import SignUpForm, PrescriptionForm
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import Group
from .forms import CheckoutForm
from pharmacy.services.order_utils import create_order_from_cart


@login_required
def product_list(request):
    products = Product.objects.all()
    return render(request, 'pharmacy/products.html', {'products': products})

@login_required
def upload_prescription(request):
    if request.method == 'POST':
        form = PrescriptionForm(request.POST, request.FILES)
        if form.is_valid():
            prescription = form.save(commit=False)
            prescription.user = request.user
            prescription.status = 'pending'
            prescription.save()
            return redirect('cart')
    else:
        form = PrescriptionForm()
    return render(request, 'pharmacy/upload_prescription.html', {'form': form})



@login_required
def add_to_cart(request, product_id):
    cart = request.session.get('cart', {})
    cart[str(product_id)] = cart.get(str(product_id), 0) + 1
    request.session['cart'] = cart
    return redirect('cart')

@login_required
def view_cart(request):
    cart = request.session.get('cart', {})
    products = Product.objects.filter(id__in=cart.keys())

    cart_items = []
    total = 0
    needs_prescription = False

    for product in products:
        quantity = cart[str(product.id)]
        subtotal = product.price * quantity
        total += subtotal
        cart_items.append({
            'product': product,
            'quantity': quantity,
            'subtotal': subtotal
        })
        if product.requires_prescription:
            needs_prescription = True


    return render(request, 'pharmacy/cart.html', {
        'cart_items': cart_items,
        'total': total,
        'needs_prescription': needs_prescription,
        # 'user_prescription': user_prescription,
    })


from .forms import CheckoutForm

@login_required
def checkout(request):
    cart = request.session.get('cart', {})
    products = Product.objects.filter(id__in=cart.keys())

    needs_prescription = any(p.requires_prescription for p in products)

    if request.method == 'POST':
        form = CheckoutForm(request.POST, request.FILES)
        if form.is_valid():
            delivery = form.cleaned_data['delivery_method']
            payment = form.cleaned_data['payment_method']

            if needs_prescription:
                if not form.cleaned_data['prescription_file']:
                    return render(request, 'pharmacy/checkout.html', {
                        'form': form,
                        'cart_items': cart,
                        'needs_prescription': True,
                        'error': 'This order requires a prescription.',
                    })

                # Create prescription and store order data in it
                prescription = Prescription.objects.create(
                    user=request.user,
                    file=form.cleaned_data['prescription_file'],
                    status='pending',
                    delivery_method=delivery,
                    payment_method=payment,
                    cart_data=cart
                )

                request.session['cart'] = {}
                return render(request, 'pharmacy/checkout_pending.html', {
                    'prescription': prescription
                })

            else:
                # No prescription needed – create order directly
                from pharmacy.services.order_utils import create_order_from_cart
                try:
                    order = create_order_from_cart(
                        user=request.user,
                        cart=cart,
                        delivery=delivery,
                        payment=payment
                    )
                except ValueError as e:
                    return render(request, 'pharmacy/checkout_blocked.html', {'message': str(e)})

                # Clear cart and redirect
                request.session['cart'] = {}
                return redirect('order_history')

    else:
        form = CheckoutForm()

    return render(request, 'pharmacy/checkout.html', {
        'form': form,
        'cart_items': cart,
        'needs_prescription': needs_prescription,
    })



@login_required
def order_history(request):
    # 1. All orders, newest first
    orders = Order.objects.filter(user=request.user).order_by('-created_at')

    # 2. Any prescriptions _not_ yet turned into an order
    prescriptions = Prescription.objects.filter(
        user=request.user,
        order__isnull=True
    ).order_by('-uploaded_at')

    return render(request, 'pharmacy/order_history.html', {
        'orders': orders,
        'prescriptions': prescriptions,
    })


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = SignUpForm()
    return render(request, 'pharmacy/signup.html', {'form': form})

@login_required
def profile(request):
    profile = request.user.userprofile
    if request.method == 'POST':
        profile.full_name = request.POST.get('full_name')
        profile.address = request.POST.get('address')
        profile.phone = request.POST.get('phone')
        profile.save()
        return redirect('profile')
    return render(request, 'pharmacy/profile.html', {'profile': profile})

def is_pharmacist(user):
    return user.groups.filter(name='Pharmacist').exists()

@user_passes_test(is_pharmacist)
def prescription_queue(request):
    prescriptions = Prescription.objects.filter(status='pending').order_by('-uploaded_at')
    return render(request, 'pharmacy/pharmacist_queue.html', {'prescriptions': prescriptions})

@user_passes_test(is_pharmacist)
def update_prescription_status(request, pk, action):
    prescription = get_object_or_404(Prescription, pk=pk)

    if action == 'approve':
        prescription.status = 'validated'

        # Load cart and fallback delivery/payment options
        cart = prescription.cart_data or {}
        delivery = prescription.delivery_method
        payment = prescription.payment_method

        # Create order
        order = Order.objects.create(
            user=prescription.user,
            is_paid=True,  # Simulate payment
            delivery_method=delivery,
            payment_method=payment,
        )

        # Bulk-fetch products
        product_ids = cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        product_map = {str(p.id): p for p in products}

        # Init total
        order_total = 0

        # Create order items and update stock
        for product_id, quantity in cart.items():
            product = product_map.get(str(product_id))
            if not product:
                continue

            if product.stock < quantity:
                return render(request, 'pharmacy/checkout_blocked.html', {
                    'message': f"Not enough stock for {product.name}."
                })

            subtotal = product.price * quantity
            order_total += subtotal

            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=quantity
            )

            product.stock -= quantity
            product.save()

        # Save total cost
        order.total = order_total
        order.save()

        # Link prescription to order
        prescription.order = order
        prescription.save()

    elif action == 'reject':
        prescription.status = 'rejected'
        prescription.save()

    return redirect('pharmacist_queue')


def role_based_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)

            print("DEBUG GROUPS:", user.groups.all())

            if user.groups.filter(name='Pharmacist').exists():
                print("REDIRECTING TO pharmacist_queue")
                return redirect('pharmacist_queue')
            else:
                print("REDIRECTING TO products")
                return redirect('products')
    else:
        form = AuthenticationForm()

    return render(request, 'pharmacy/login.html', {'form': form})

@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'pharmacy/order_detail.html', {'order': order})

@login_required
def increase_quantity(request, product_id):
    cart = request.session.get('cart', {})
    cart[str(product_id)] = cart.get(str(product_id), 0) + 1
    request.session['cart'] = cart
    return redirect('cart')

@login_required
def decrease_quantity(request, product_id):
    cart = request.session.get('cart', {})
    if str(product_id) in cart:
        cart[str(product_id)] -= 1
        if cart[str(product_id)] <= 0:
            del cart[str(product_id)]
    request.session['cart'] = cart
    return redirect('cart')

@login_required
def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})
    cart.pop(str(product_id), None)
    request.session['cart'] = cart
    return redirect('cart')