from django.urls import path
from .views import cart_view, add_to_cart, update_cart, remove_from_cart, clear_cart, checkout_cart

urlpatterns = [
    path('', cart_view, name='cart'),
    path('add/<int:pk>/', add_to_cart, name='add_to_cart'),
    path('update/<int:pk>/<str:action>/', update_cart, name='update_cart'),
    path('remove/<int:pk>/', remove_from_cart, name='remove_from_cart'),
    path('clear/', clear_cart, name='clear_cart'),
    path('checkout/', checkout_cart, name='checkout_cart'),
]
