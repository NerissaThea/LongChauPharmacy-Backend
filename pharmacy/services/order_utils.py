from pharmacy.models import Order, OrderItem, Product

def create_order_from_cart(user, cart, delivery, payment):
    product_ids = cart.keys()
    products = Product.objects.filter(id__in=product_ids)
    product_map = {str(p.id): p for p in products}

    order = Order.objects.create(
        user=user,
        is_paid=True,
        delivery_method=delivery,
        payment_method=payment,
    )

    order_total = 0

    for product_id, quantity in cart.items():
        product = product_map.get(str(product_id))
        if not product:
            continue

        if product.stock < quantity:
            raise ValueError(f"Not enough stock for {product.name}")

        subtotal = product.price * quantity
        order_total += subtotal

        OrderItem.objects.create(order=order, product=product, quantity=quantity)
        product.stock -= quantity
        product.save()

    order.total = order_total
    order.save()
    return order
