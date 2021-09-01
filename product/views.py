from django.shortcuts import render, redirect
from .models import *
from django.shortcuts import get_object_or_404
# from django.views.generic import DetailView
# from analytics.mixins import ObjectViewedMixin
# from cart.models import Cart

# Create your views here.

def product_details(request, cat_slug, subcat_slug, brand_slug, product_slug):
    product = Product.objects.get(slug=product_slug)
    context = {
        'product':product
    }
    return render(request, 'product_details.html', context)

def add_to_history(request, id):
    if request.method == "POST":
        if not request.session.get('product_history'):
            request.session['product_history'] = list()
        else:
            request.session['product_history'] = list(request.session['product_history'])
    products = next((item for item in request.session['product_history'] if item['id']==id),False)
    add_product = {
        'id':id,
    }
    if not products:
        request.session['product_history'].append(add_product)
        request.session.modifier = True

    return redirect('index')

# class ProductDetail(ObjectViewedMixin, DetailView):
#     queryset = Product.objects.all()
#     template_name = 'product.html'

#     def get_context_data(self, **kwargs):
#         context = super(ProductDetail, self).get_context_data(**kwargs)
#         context["cart"] = 'okey' # niye 'okey' yazmisiq bura?)
#         return context

#     def get_object(self, *args, **kwargs):
#         request = self.request
#         id = self.kwargs.get('id')
#         instance = Product.objects.get(id=id)
#         return instance


# def product(request):
#     products = Product.objects.all()
#     context = {
#         'products': products,
#         'user': request.user
#     }
#     return render(request, 'product.html', context)