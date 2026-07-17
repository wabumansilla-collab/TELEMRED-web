from django.urls import path
from .views import quote_form

urlpatterns = [
    path('', quote_form, name='quote_form'),
]
