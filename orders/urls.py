from django.urls import path
from orders.views import checkout_reuse_address, checkout_create_address
urlpatterns = [
    path('checkout/address/create/', checkout_create_address, name="checkout_create_address"),
    path('checkout/address/reuse/', checkout_reuse_address, name='checkout_reuse_address'),
]
