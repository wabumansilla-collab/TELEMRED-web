from django.contrib import admin
from .models import Category, Product, Cart, CartItem, Quote, Discount, Sale, SaleItem

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')
    search_fields = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category', 'type', 'price', 'stock', 'is_active', 'created_at')
    list_filter = ('is_active', 'type', 'category')
    search_fields = ('name', 'description')
    list_editable = ('price', 'stock', 'is_active')
    ordering = ('-created_at',)
    fieldsets = (
        ('Información General', {
            'fields': ('name', 'category', 'type', 'description', 'image')
        }),
        ('Inventario y Precio', {
            'fields': ('price', 'stock', 'is_active')
        }),
    )

class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'created_at')
    inlines = [CartItemInline]

@admin.register(Quote)
class QuoteAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'user', 'created_at', 'is_processed')
    list_filter = ('is_processed', 'created_at')
    search_fields = ('title', 'description')
    list_editable = ('is_processed',)
    readonly_fields = ('created_at', 'updated_at')

@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    list_display = ('code', 'discount_type', 'value', 'valid_from', 'valid_until', 'is_active')
    list_filter = ('is_active', 'discount_type')
    search_fields = ('code',)

class SaleItemInline(admin.TabularInline):
    model = SaleItem
    extra = 0

@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'total_amount', 'is_paid', 'created_at')
    list_filter = ('is_paid', 'created_at')
    inlines = [SaleItemInline]
