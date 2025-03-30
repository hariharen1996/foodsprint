from django.contrib import admin
from .models import Category,FoodItems,Cart,CartItem

# Register your models here.
admin.site.register(Category)
admin.site.register(FoodItems)
admin.site.register(Cart)
admin.site.register(CartItem)
