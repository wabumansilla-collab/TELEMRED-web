from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# Personalización del Panel de Administración TELEMRED
admin.site.site_header = 'TELEMRED - Administración Central'
admin.site.site_title = 'TELEMRED Admin'
admin.site.index_title = 'Gestión de Catálogo, Cotizaciones y POS'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.core.urls')),
    path('shop/', include('apps.shop.urls')),
    path('cart/', include('apps.cart.urls')),
    path('quotes/', include('apps.quotes.urls')),
    path('customers/', include('apps.customers.urls')),
    path('pos/', include('apps.pos.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
