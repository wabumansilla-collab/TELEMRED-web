from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from apps.shop.models import Quote, Sale

def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
        
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f"¡Bienvenido nuevamente a TELEMRED, {user.username}!")
            return redirect('dashboard')
        else:
            messages.error(request, "Credenciales incorrectas. Verifique su usuario y contraseña.")
            
    return render(request, 'customers/login.html')

def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
        
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '').strip()
        password_confirm = request.POST.get('password_confirm', '').strip()
        
        if not username or not email or not password:
            messages.error(request, "Todos los campos son requeridos para el registro de cliente.")
            return render(request, 'customers/register.html')
            
        if password != password_confirm:
            messages.error(request, "Las contraseñas ingresadas no coinciden.")
            return render(request, 'customers/register.html')
            
        if User.objects.filter(username__iexact=username).exists():
            messages.error(request, "El nombre de usuario ingresado ya se encuentra registrado.")
            return render(request, 'customers/register.html')
            
        user = User.objects.create_user(username=username, email=email, password=password)
        login(request, user)
        messages.success(request, "¡Registro de cuenta corporativa exitoso! Ahora tiene acceso completo al Portal de Clientes.")
        return redirect('dashboard')
        
    return render(request, 'customers/register.html')

def dashboard_view(request):
    if not request.user.is_authenticated:
        # Modo demostración si no ha iniciado sesión para que el usuario siempre vea la estética y funcionalidad
        return render(request, 'customers/dashboard.html', {
            'is_demo': True,
            'demo_quotes': [
                {'title': '[Red Corporativa] Anillo 10G FTTH Planta Sur', 'created_at': 'Hoy', 'status': 'En Análisis Técnico NOC'},
                {'title': '[Ciberseguridad] Auditoría Perimetral FortiGate 60F', 'created_at': '12 de Jul', 'status': 'Cotización Emitida ($1,450)'}
            ]
        })
        
    user_quotes = Quote.objects.filter(user=request.user).order_by('-created_at')[:10]
    user_sales = Sale.objects.filter(user=request.user).order_by('-created_at')[:10]
    
    return render(request, 'customers/dashboard.html', {
        'is_demo': False,
        'user_quotes': user_quotes,
        'user_sales': user_sales,
        'cart_count': len(request.session.get('cart', {}))
    })

def logout_view(request):
    logout(request)
    messages.info(request, "Ha cerrado sesión de forma segura.")
    return redirect('home')
