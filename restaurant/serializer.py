from rest_framework import serializers
from .models import Category,FoodItems,Cart,CartItem

class CatgeorySerailizer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name','description','created_at','updated_at']
        read_only_fields = ('created_at','updated_at')
        
class FoodItemSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())

    def validate(self, attrs):
        if 'category' not in attrs:
            raise serializers.ValidationError('Category is required')

        if not Category.objects.filter(id=attrs['category'].id).exists():
            raise serializers.ValidationError('Category does not exists')

        return attrs

    class Meta:
        model = FoodItems
        fields = '__all__'
        read_only_fields = ('created_at','updated_at')

class CartItemSerializer(serializers.ModelSerializer):
    food_item = FoodItemSerializer(read_only=True)
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = ['id','food_item','quantity','total_price']
        read_only_fields = ('total_price',)
    
    def get_total_price(self,data):
        return data.total_price

class CartSerailizer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True,read_only=True)
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ['id','items','total_price','created_at','updated_at']
        read_only_fields = ('user','total_price')
    
    def get_total_price(self,data):
        return data.total_price 

class AddToCartSerializer(serializers.ModelSerializer):
    food_item_id = serializers.IntegerField()
    quantity = serializers.IntegerField(default=1)

    def validate_food_item_id(self,value):
        if not FoodItems.objects.filter(pk=value).exists():
            raise serializers.ValidationError('Food item does not exits')
        return value 
    
    def save(self,**kwargs):
        user = self.context['request'].user 
        food_item_id = self.validated_data['food_item_id']
        quantity = self.validated_data['quantity']

        cart,_ = Cart.objects.get_or_create(user=user)

        cart_item,created = CartItem.objects.get_or_create(cart=cart,food_item_id=food_item_id,defaults={'quantity':quantity})

        if not created:
            cart_item.quantity = quantity
            cart_item.save()

        return cart
    
class UpdateCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem 
        fields = ['quantity']     