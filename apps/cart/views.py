from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from apps.shop.models import Product, Discount
from django.utils import timezone

def _get_cart_session(request):
    if 'cart' not in request.session:
        request.session['cart'] = {}
    return request.session['cart']

def cart_view(request):
    cart_session = _get_cart_session(request)
    cart_items = []
    total_amount = 0

    product_ids = cart_session.keys()
    products = Product.objects.filter(pk__in=product_ids)
    product_dict = {str(p.pk): p for p in products}

    for str_id, quantity in cart_session.items():
        product = product_dict.get(str_id)
        if product:
            subtotal = float(product.price) * quantity
            total_amount += subtotal
            cart_items.append({
                'product': product,
                'quantity': quantity,
                'subtotal': subtotal
            })

    discount_amount = 0
    discount_code = request.GET.get('discount') or request.session.get('applied_discount_code')
    if discount_code:
        try:
            discount = Discount.objects.get(code__iexact=discount_code, is_active=True, valid_until__gte=timezone.now())
            if discount.discount_type == 'percentage':
                discount_amount = total_amount * (float(discount.value) / 100.0)
            else:
                discount_amount = float(discount.value)
            request.session['applied_discount_code'] = discount.code
            messages.success(request, f"Código de descuento '{discount.code}' aplicado exitosamente (-${discount_amount:.2f}).")
        except Discount.DoesNotExist:
            if request.GET.get('discount'):
                messages.error(request, "El código de descuento ingresado no es válido o ha expirado.")

    final_total = max(0, total_amount - discount_amount)
    iva = final_total * 0.19  # 19% IVA en Chile
    total_with_iva = final_total + iva

    return render(request, 'cart/cart.html', {
        'cart_items': cart_items,
        'total_amount': total_amount,
        'discount_amount': discount_amount,
        'final_total': final_total,
        'iva': iva,
        'total_with_iva': total_with_iva
    })

def add_to_cart(request, pk):
    product = get_object_or_404(Product, pk=pk)
    cart = _get_cart_session(request)
    str_id = str(product.pk)

    if str_id in cart:
        cart[str_id] += 1
    else:
        cart[str_id] = 1

    request.session['cart'] = cart
    request.session.modified = True
    messages.success(request, f"'{product.name}' fue añadido a su carrito.")
    
    # Redirigir según la página de origen o al carrito
    referer = request.META.get('HTTP_REFERER')
    if referer and '/shop/' in referer:
        return redirect(referer)
    return redirect('cart')

def update_cart(request, pk, action):
    cart = _get_cart_session(request)
    str_id = str(pk)

    if str_id in cart:
        if action == 'add':
            cart[str_id] += 1
        elif action == 'sub':
            cart[str_id] -= 1
            if cart[str_id] <= 0:
                del cart[str_id]
        request.session['cart'] = cart
        request.session.modified = True
        
    return redirect('cart')

def remove_from_cart(request, pk):
    cart = _get_cart_session(request)
    str_id = str(pk)
    if str_id in cart:
        del cart[str_id]
        request.session['cart'] = cart
        request.session.modified = True
        messages.success(request, "Ítem eliminado del carrito.")
    return redirect('cart')

def clear_cart(request):
    request.session['cart'] = {}
    if 'applied_discount_code' in request.session:
        del request.session['applied_discount_code']
    request.session.modified = True
    messages.info(request, "El carrito ha sido vaciado.")
    return redirect('cart')

def checkout_cart(request):
    cart = _get_cart_session(request)
    if not cart:
        messages.error(request, "Tu carrito está vacío. Agrega ítems antes de proceder al pago.")
        return redirect('shop_list')
    
    # Simular orden de compra en el sistema
    request.session['cart'] = {}
    if 'applied_discount_code' in request.session:
        del request.session['applied_discount_code']
    request.session.modified = True
    
    messages.success(request, "🎉 ¡Orden de compra procesada con éxito! Nuestro departamento de ingeniería se contactará con usted en breve para la coordinación logística.")
    return redirect('home')
