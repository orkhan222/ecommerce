from backend.models import User
from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from category.models import *
from staticpage.models import *
from product.models import Product
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import *
from rest_framework import permissions, viewsets, status
from typing import ItemsView
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
class ModelViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializers
    queryset = Product.objects.all()

class ProductViews(APIView):
    def get(self,request):
        products = Product.objects.all()
        serializer = ProductSerializers(products, many=True)
        return Response(serializer.data)

    def post(self,request):
        serializer = ProductSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)


class ProductDetailViews(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self,request,id):
        product = Product.objects.get(id=id)
        serializer = ProductDetailSerializers(product)
        return Response(serializer.data)

    def put(self,request,id):
        if request.user.is_delivery():
            product = Product.objects.get(id=id)
            serializer = ProductSerializers(product,data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors)
        return Response(status=status.HTTP_409_CONFLICT)

    def delete(self,request,id):
        product = Product.objects.get(id=id)
        del product
        return Response({"success":"Product deleted!"})

def index(request):
    categories = Category.objects.prefetch_related('sub_categories').all()
    sliders = Slider.objects.all()
    #request.session['test'] = 10
    print(request.session.items())
    products = Product.objects.all()[:10]
    context = {
        'categories':categories,
        'sliders':sliders,
        'products':products, 
    }
    return render(request,'index.html', context)
    
@csrf_exempt
def add_to_wishlist(request,id):
    if request.method == "POST":
        if not request.session.get('wishlist'):
            request.session['wishlist'] = list()
        else:
            request.session['wishlist'] = list(request.session['wishlist'])
        items = next((item for item in request.session['wishlist'] if item['id']==id),False)
    add_data = {
        'id':id,
    }
    if not items:
        request.session['wishlist'].append(add_data)
        request.session.modifier = True
    return redirect('index')

@csrf_exempt
def remove_wishlist(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        for i in request.session['wishlist']:
            if str(i['id']) == id:
                i.clear()
        while {} in request.session['wishlist']:
            request.session['wishlist'].remove({})
        if not request.session['wishlist']:
            del request.session['wishlist']
    try:
        request.session['wishlist'] = list(request.session['wishlist'])
    except:
        pass
    request.session.modifier = True
    return JsonResponse({'status':'ok'})

import datetime
from datetime import date, datetime, timedelta
from django.conf import settings
import jwt
from backend.models import User
from django.contrib.auth import authenticate

def create_verify_token(id):
        dt = datetime.now() + timedelta(days=60)
        token = jwt.encode({
            "id": id,
            "exp": int(dt.timestamp())
        },settings.SECRET_KEY,algorithm='HS256')
        return token


@csrf_exempt
def token_very(request):
    # return JsonResponse ({"data":str(datetime.datetime.now())}) 
    # return HttpResponse(str(datetime.datetime.now()))
    # return JsonResponse ({"data":str(dir(request))})
    # return JsonResponse ({"data":str(request.GET.get('name'))}) 
    if request.method == 'POST':
        user = authenticate(email=request.POST.get('email'),password=request.POST.get('password'))
        if user is not None:
        # user = User.objects.get(email=request.POST.get('email'))
            token = create_verify_token(user.id)
            print(token)
            return JsonResponse ({"data":str("token")}) 
        else:
            return JsonResponse ({"eror":str("No auth")}) 




# def get_func(request):
#     price = request.GET.get('price')
#     price_to = request.GET.get('price_to')
#     print(price,price_to)
#     product = Product.objects.all()
#     brand = request.GET.get('brand')
#     color = request.GET.get('color')
#     print(color)
#     if price and price_to is not None:
#         product = Product.objects.filter(product_price__gte=price, product_price__lte=price_to)
#         product.filter()
#     if brand is not None:
#         product = Product.objects.filter(product_brand=brand)
#     if color is not None:
#         product = Product.objects.filter(product_descrption__in=color.rsplit(','))
        
#         context = {
#             'product':product
#         }
#     return render(request,'product.html',context)

def get_func(request):
    data= dict(request.GET)
    try:
        data['product_price_gte'] = request.GET.get('product_price_gte')
        data['product_price_lte'] = request.GET.get('product_price_lte')
        print(data)
    except:
        pass
    product = Product.objects.all()
    if len(data) > 2:
        product = Product.objects.filter(**data)
        
    context = {
        'product':product
    }
    return render(request,'product.html',context)
    