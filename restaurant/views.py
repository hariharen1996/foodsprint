from django.shortcuts import render
from rest_framework import status 
from rest_framework.generics import ListCreateAPIView,RetrieveUpdateDestroyAPIView,RetrieveAPIView,GenericAPIView,UpdateAPIView,DestroyAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Cart,CartItem,Category,FoodItems
from .serializer import CartSerailizer,CatgeorySerailizer,AddToCartSerializer,FoodItemSerializer,UpdateCartItemSerializer

# Create your views here.
class CategoryListCreateAPIView(ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CatgeorySerailizer
    permission_classes = [IsAuthenticated]

class CategoryRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CatgeorySerailizer 
    permission_classes = [IsAuthenticated]

class FoodItemListCreateAPIView(ListCreateAPIView):
    queryset = FoodItems.objects.select_related('category').all()
    serializer_class = FoodItemSerializer
    permission_classes = [IsAuthenticated]

class FoodItemsRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = FoodItems.objects.select_related('category').all()
    serializer_class = FoodItemSerializer
    permission_classes = [IsAuthenticated]
    
class CartView(RetrieveAPIView):
    serializer_class = CartSerailizer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        cart,created = Cart.objects.get_or_create(user=self.request.user)
        return cart 

class AddToCartView(GenericAPIView):
    serializer_class = AddToCartSerializer
    permission_classes = [IsAuthenticated]

    def post(self,request,*args,**kwargs):
        serializer = serializer.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        cart,created = Cart.objects.get_or_create(user=request.user)
        food_items_id = serializer.validated_data['food_item_id']
        quantity = serializer.validated_data['quantity']

        cart_item,created = CartItem.objects.get_or_create(cart=cart,food_items_id=food_items_id,defaults={'quantity':quantity})

        if not created:
            cart_item.quantity += quantity
            cart_item.save()

        return Response({'detail':'items added to cart successfully'},status=status.HTTP_200_OK)
    
class UpdateCartItemView(UpdateAPIView):
    serializer_class = UpdateCartItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        cart,created = Cart.objects.get_or_create(user=self.request.user)
        return CartItem.objects.filter(cart=cart)
    
    def perform_update(self, serializer):
        if serializer.validated_data['quantity'] <= 0:
            self.get_object().delete()
        else:
            serializer.save()

class RemoverCartView(DestroyAPIView):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        cart,created = Cart.objects.get_or_create(user=self.request.user)
        return CartItem.objects.filter(cart=cart)
    
