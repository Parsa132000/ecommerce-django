from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet, ProductViewSet, VendorViewSet, OrderViewSet , CartViewSet,CartItemViewSet

router = DefaultRouter()
router.register('categories', CategoryViewSet)
router.register('products', ProductViewSet)
router.register('vendors', VendorViewSet)
router.register('orders', OrderViewSet)
router.register('cart', CartViewSet)
router.register('cart-items', CartItemViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
