from django.urls import path
from .views import pos_view

urlpatterns = [
    path('', pos_view, name='pos'),
]
