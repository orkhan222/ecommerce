from django.urls import path, include
from .views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'model', ModelViewSet, basename="model")

urlpatterns = [
    path('api/v1/', include(router.urls)),
    path('', index, name='index'),
    path('add_to_wishlist/<int:id>/', add_to_wishlist, name='add_to_wishlist'),
    path('remove_wishlist/', remove_wishlist, name='remove_wishlist'),
    path('api/product/', ProductViews.as_view()),
    path('api/product/<int:id>', ProductDetailViews.as_view()),
    path('api/token',token_very),
]