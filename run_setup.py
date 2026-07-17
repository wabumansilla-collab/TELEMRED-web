#!/usr/bin/env python
"""
Script de inicialización automática de TELEMRED.
Ejecutar con: python run_setup.py
"""
import os
import sys
import django

# Forzar salida en UTF-8 o reemplazar caracteres no soportados
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'telemred.settings')
django.setup()

from django.core.management import call_command
from apps.shop.models import Product, Category
from apps.shop.views import ensure_admin_and_initial_categories
from django.contrib.auth.models import User

def main():
    print("[1/3] Detectando y verificando migraciones en la base de datos...")
    try:
        call_command('makemigrations', 'shop', 'core', 'cart', 'quotes', 'customers', 'pos')
        call_command('makemigrations')
    except Exception as e:
        print(f"Nota en migraciones: {e}")
    
    print("[2/3] Aplicando migraciones a db.sqlite3...")
    try:
        call_command('migrate')
    except Exception as e:
        print(f"Nota en migrate: {e}")
    
    print("[3/3] Configurando usuario Administrador (admin / admin1365) y dejando catálogo en blanco...")
    ensure_admin_and_initial_categories()
    
    total_products = Product.objects.count()
    total_categories = Category.objects.count()
    admin_exists = User.objects.filter(username='admin').exists()
    
    print(f"\n¡Proyecto TELEMRED reconfigurado exitosamente!")
    print(f"Usuario Administrador verificado: {'SI (user: admin | pass: admin1365)' if admin_exists else 'NO'}")
    print(f"Catalogo en blanco: {total_products} productos activos | {total_categories} categorias base disponibles para asignacion.")
    print("\nPara ejecutar el servidor, ingrese el comando: python manage.py runserver")

if __name__ == '__main__':
    main()
