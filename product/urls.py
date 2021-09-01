from django.urls import path
from .views import *

urlpatterns = [
    path('<cat_slug>/<subcat_slug>/<brand_slug>/<product_slug>/', product_details, name='product_details'),
    path('add_to_history/<int:id>/', add_to_history, name='add_to_history'),
]