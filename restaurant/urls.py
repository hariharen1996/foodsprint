from django.urls import path,include
from .views import (
    CategoryListCreateAPIView,CategoryRetrieveUpdateDestroyAPIView,FoodItemListCreateAPIView,FoodItemsRetrieveUpdateDestroyAPIView,
    CartView,AddToCartView,UpdateCartItemView,RemoverCartView
)
urlpatterns = [
    path('categories/',CategoryListCreateAPIView.as_view(),name='category-list'),
    path('categories/<int:pk>',CategoryRetrieveUpdateDestroyAPIView.as_view(),name='category-details'),
    path('food-items/',FoodItemListCreateAPIView.as_view(),name='food-items'),
    path('food-items/<int:pk>',FoodItemsRetrieveUpdateDestroyAPIView.as_view(),name='food-items-details'),
    path('cart/',CartView.as_view(),name='carts'),
    path('cart/add/',AddToCartView.as_view(),name='add-cart'),
    path('cart/items/<int:pk>/',UpdateCartItemView.as_view(),name='update-cart'),
    path('cart/items/<int:pk>/remove/',RemoverCartView.as_view(),name='remove-cart'),
]
