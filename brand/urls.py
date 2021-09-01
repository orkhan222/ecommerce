from django.urls import path
from .views import *

urlpatterns = [
    path('<cat_slug>/<subcat_slug>/<brand_slug>', brand_products, name='brand_products'),
]
