from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Vendor, Category, Product, Order, OrderItem

admin.site.register(User, UserAdmin)
admin.site.register(Vendor)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderItem)
