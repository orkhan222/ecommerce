from django.shortcuts import render, redirect
from .models import Product, CartProduct, Cart
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

# Create your views here.

def cart_products(request):
    products = []
    total = 0
    for product in request.session['cart']:
        p_data = dict(product)
        id = p_data['id']
        quantity = p_data['quantity']
        obj = Product.objects.get(id=id)
        products.append((obj,quantity))
        if obj.product_discount :
            total += obj.product_discount_price * quantity
        else :
            total += obj.product_price * quantity
    context = {
        'products':products,
        'total':total
    }
    return render(request, 'cart_products.html', context)
    
@csrf_exempt
def add_to_cart(request, id):
    if request.method == "POST":
        if not request.session.get('cart'):
            request.session['cart'] = list()
        else:
            request.session['cart'] = list(request.session['cart'])
    products = next((item for item in request.session['cart'] if item['id']==id),False)
    add_product = {
        'id':id,
        'quantity':1
    }
    if not products:
        request.session['cart'].append(add_product)
        request.session.modifier = True

    return redirect('cart_products')

@csrf_exempt
def change_quantity(request, id, qyt):
    id = int(id)
    qyt = int(qyt)
    if request.method == 'POST':
        new_session_data = []
        for product in request.session['cart']:
            p_data = dict(product)
            p_id = p_data['id']
            if p_id == id:
                p_data['quantity'] = qyt
            new_session_data.append(p_data)
        request.session['cart'] = new_session_data
        print(new_session_data)
    return redirect('cart_products')

@csrf_exempt
def confirm_cart(request):
    products = []
    for product in request.session['cart']:
        id = product['id']
        quantity = product['quantity']
        obj = Product.objects.get(id=id)
        products.append((obj,quantity))
    context = {
        'products':products,
    }
    if request.method == 'GET':
        cart_products = []
        for product in products:
            p_data = list(product)
            cart_product,cart_product_value = CartProduct.objects.get_or_create(product=p_data[0], quantity=p_data[1])
            cart_products.append(cart_product.id)
        #print(request.session['cart_id'])
        cart = Cart.object.new_or_get(request)
        for c in cart_products:
            cart[0].products.add(c)
            request.session['cart_id'] = cart[0].id

    return render(request, 'confirm_cart.html', context)

def cart_remove(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        for i in request.session['cart']:
            if str(i['id']) == id:
                i.clear()
        while {} in request.session['cart']:
            request.session['cart'].remove({})
        if not request.session['cart']:
            del request.session['cart']
    try:
        request.session['cart'] = list(request.session['cart'])
    except:
        pass
    request.session.modifier = True
    return JsonResponse({'status':'ok'})