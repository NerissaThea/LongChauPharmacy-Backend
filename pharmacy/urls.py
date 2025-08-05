from django.urls import path
from django.http import HttpResponse
from . import views
from django.contrib.auth import views as auth_views

def home(request):
    return HttpResponse("Hello from Pharmacy app!")

urlpatterns = [
    path('', views.product_list, name='products'),  # default page
    path('products/', views.product_list, name='products'),
    path('login/', views.role_based_login, name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('upload/', views.upload_prescription, name='upload_prescription'),
    path('cart/', views.view_cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('orders/', views.order_history, name='order_history'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('signup/', views.signup, name='signup'),
    path('profile/', views.profile, name='profile'),
    path('pharmacist/prescriptions/', views.prescription_queue, name='pharmacist_queue'),
    path('pharmacist/prescription/<int:pk>/<str:action>/', views.update_prescription_status, name='prescription_action'),
    path('orders/<int:order_id>/', views.order_detail, name='order_detail'),
    path('cart/increase/<int:product_id>/', views.increase_quantity, name='cart_increase'),
    path('cart/decrease/<int:product_id>/', views.decrease_quantity, name='cart_decrease'),
    path('cart/remove/<int:product_id>/', views.remove_from_cart, name='cart_remove'),



]
