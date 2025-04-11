from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']  # username is still required for now

    def __str__(self):
        return self.email



class Vendor(models.Model):
    user = models.OneToOneField('core.User', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    contact_email = models.EmailField()

    def __str__(self):
        return self.name



class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name
    
    
    
    
class Product(models.Model):
    vendor = models.ForeignKey('core.Vendor', on_delete=models.CASCADE, related_name='products')
    category = models.ForeignKey('core.Category', on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    inventory = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name



class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('shipped', 'Shipped'),
        ('completed', 'Completed'),
        ('canceled', 'Canceled'),
    ]

    user = models.ForeignKey('core.User', on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order #{self.pk} by {self.user.email}"








class OrderItem(models.Model):
    order = models.ForeignKey('core.Order', on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey('core.Product', on_delete=models.SET_NULL, null=True)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)  # capture at time of order

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"






class Cart(models.Model):
    user = models.OneToOneField('core.User', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email}'s Cart"





class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ('cart', 'product')

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"


