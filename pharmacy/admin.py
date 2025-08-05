from django.contrib import admin
from .models import Product, Prescription, Order, OrderItem

admin.site.register(Product)
admin.site.register(Prescription)
admin.site.register(Order)
admin.site.register(OrderItem)
