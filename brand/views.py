from django.shortcuts import render
from category.models import *
from brand.models import *

# Create your views here.

def brand_products(request, cat_slug, subcat_slug, brand_slug):
    products = Brand.products_in_brand(brand_slug)
    context = {
        'products':products
    }
    return render(request, 'brand_products.html', context)

