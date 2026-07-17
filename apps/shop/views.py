from django.shortcuts import render, get_object_or_404
from .models import Product, Category
from django.contrib.auth.models import User

def ensure_admin_and_initial_categories():
    """Asegura la existencia del administrador (user: admin, pass: admin1365) y elimina productos autogenerados de prueba para dejar el catálogo en blanco según requerimiento."""
    try:
        # Asegurar usuario administrador solicitado (admin / admin1365)
        admin_user, created = User.objects.get_or_create(username='admin', defaults={'email': 'admin@telemred.cl'})
        if created or not admin_user.is_superuser:
            admin_user.is_staff = True
            admin_user.is_superuser = True
            admin_user.set_password('admin1365')
            admin_user.save()
        else:
            # Asegurar que la contraseña es exactamente admin1365
            if not admin_user.check_password('admin1365'):
                admin_user.set_password('admin1365')
                admin_user.save()

        # Eliminar productos autogenerados si existen ("OLT GPON...", etc.) para dejar el catálogo en blanco
        dummy_names = [
            'OLT GPON 8 Puertos Carrier-Class con Doble Fuente SFP+',
            'Router Core Cloud Core CCR2116-12G-4S+ Mikrotik',
            'Firewall FortiGate 60F Next-Gen Security Appliance',
            'Bobina Cable Fibra Óptica Drop FTTH 1000m Monomodo G.657A1',
            'Servicio Certificación OTDR y Fusión de Fibra Óptica (por Hilo)',
            'Switch Administrable 24 Puertos PoE+ Gigabit 370W + 4 SFP+',
            'Auditoría Integral de Ciberseguridad & Test de Intrusión (Pentest)',
            'Gabinete de Telecomunicaciones de Piso 42U 600x800mm con Ventilación'
        ]
        Product.objects.filter(name__in=dummy_names).delete()

        # Asegurar categorías base para facilitar la creación desde el admin
        Category.objects.get_or_create(name='Equipos de Red & Routers', slug='equipos-red')
        Category.objects.get_or_create(name='Fibra Óptica & FTTH', slug='fibra-optica')
        Category.objects.get_or_create(name='Ciberseguridad & Firewalls', slug='ciberseguridad')
        Category.objects.get_or_create(name='Servicios e Ingeniería', slug='servicios')
    except Exception:
        pass

def product_list(request):
    ensure_admin_and_initial_categories()
    products = Product.objects.filter(is_active=True).select_related('category')
    categories = Category.objects.all()
    
    category_slug = request.GET.get('category')
    if category_slug:
        products = products.filter(category__slug=category_slug)
        
    return render(request, 'shop/product_list.html', {
        'products': products,
        'categories': categories,
        'selected_category': category_slug
    })

def product_detail(request, pk):
    ensure_admin_and_initial_categories()
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'shop/product_detail.html', {'product': product})
