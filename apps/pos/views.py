from django.shortcuts import render, redirect
from django.contrib import messages
from apps.shop.models import Product
from apps.shop.views import ensure_admin_and_initial_categories

def pos_view(request):
    ensure_admin_and_initial_categories()
    
    # Verificación de exclusividad para administrador ('admin' o staff/superuser)
    if not request.user.is_authenticated or not (request.user.is_staff or request.user.is_superuser or request.user.username == 'admin'):
        messages.error(request, "⚠️ Acceso denegado: La Terminal POS es de uso exclusivo para el usuario administrador ('admin'). Inicie sesión con sus credenciales administrativas.")
        return redirect('login')

    products = Product.objects.filter(is_active=True).select_related('category')
    return render(request, 'pos/pos.html', {'products': products})
