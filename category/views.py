from django.shortcuts import render, redirect
from category.models import *

# Create your views here.

def category(request):
    category = Category.objects.all()
    context = {
        'category':category
    }
    return render(request, 'category.html', context)

def category_subcategories(request, cat_slug):
    subcategories = Category.subcategories_in_category(cat_slug)
    context = {
        'subcategories':subcategories
    }
    return render(request, 'category_subcategories.html', context)

def subcategory_brands(request, cat_slug, subcat_slug):
    brands = SubCategory.brands_in_subcategory(subcat_slug)
    context = {
        'brands':brands
    }
    return render(request, 'subcategory_brands.html', context)

