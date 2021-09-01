from django.shortcuts import render
from .models import *
from .forms import *
from address.models import Address

# Create your views here.

def order(request):
    f = OrderForm(request.POST)
    billing_address = Address.objects.filter(billing_profile__user=request.user).filter(address_type='billing')
    shipping_address = Address.objects.filter(billing_profile__user=request.user).filter(address_type='shipping')
    billing_profile_id = request.user.billing_user.id
    if request.method == "POST":
        if f.is_valid():
            obj = f.save(commit=False)
            obj.shipping_address_id = request.POST['shipping_address']
            obj.billing_address_id = request.POST['billing_address']
            obj.billing_profile_id = billing_profile_id
            obj.cart_id = request.session.get('cart_id')
            path = request.POST.get('path')
            obj.save()
            return redirect(path)
    context = {
        'f':f,
        'billing_address':billing_address,
        'shipping_address':shipping_address,
    }
    return render(request,'order.html',context)