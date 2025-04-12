from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from .models import Category, Product, Vendor, Order,Cart,CartItem,OrderItem
from .serializers import CategorySerializer, ProductSerializer, VendorSerializer, OrderSerializer,CartSerializer,CartItemSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
import stripe
from django.conf import settings
from rest_framework.views import APIView
from django.http import HttpResponse


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class VendorViewSet(viewsets.ModelViewSet):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer




class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['post'], url_path='checkout')
    def checkout(self, request):
        user = request.user
        try:
            cart = Cart.objects.get(user=user)
        except Cart.DoesNotExist:
            return Response({'error': 'Cart not found.'}, status=status.HTTP_404_NOT_FOUND)

        if cart.items.count() == 0:
            return Response({'error': 'Cart is empty.'}, status=status.HTTP_400_BAD_REQUEST)

        # Create the order
        order = Order.objects.create(user=user)

        for item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price
            )

        # Optional: clear the cart after checkout
        cart.items.all().delete()

        return Response({'message': 'Checkout successful.', 'order_id': order.id}, status=status.HTTP_201_CREATED)
class CartItemViewSet(viewsets.ModelViewSet):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return CartItem.objects.filter(cart__user=self.request.user)
    
    
    
    
    
    
    
class StripeCheckoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user

        try:
            cart = Cart.objects.get(user=user)
            if cart.items.count() == 0:
                return Response({'error': 'Cart is empty.'}, status=400)
        except Cart.DoesNotExist:
            return Response({'error': 'No cart found.'}, status=404)

        stripe.api_key = settings.STRIPE_SECRET_KEY

        line_items = []
        for item in cart.items.all():
            line_items.append({
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': item.product.name,
                    },
                    'unit_amount': int(item.product.price * 100),
                },
                'quantity': item.quantity,
            })

        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=line_items,
            mode='payment',
            success_url='http://localhost:8000/success/',
            cancel_url='http://localhost:8000/cancel/',
        )

        return Response({'url': checkout_session.url})
    
    
    
    
    
    
    

def home_view(request):
    return HttpResponse("""
        <h1>🛒 Welcome to Ecommerce API</h1>
        <p>This is a Django + DRF multi-vendor e-commerce backend.</p>
        <p>Use the <a href="/api/">API explorer</a> to try endpoints.</p>
    """)
    
