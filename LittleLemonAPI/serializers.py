from rest_framework import serializers 
from .models import MenuItem, Category, Cart, Order, OrderItem 
from django.contrib.auth.models import User

class CategorySerializer(serializers.ModelSerializer): 
    class Meta: 
        model = Category
        fields = ['id', 'title'] 

class MenuItemSerializer(serializers.ModelSerializer): 
    category_id = serializers.IntegerField()  

    class Meta: 
        model = MenuItem 
        fields = ['id', 'title', 'price',   'category_id', 'featured']

class UserSerializer(serializers.ModelSerializer):  
    
    class Meta: 
        model = User 
        fields = ('id', 'username')

class CartSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(read_only=True)
    menuitem_id = serializers.IntegerField()
    unit_price = serializers.DecimalField(max_digits=6, decimal_places=2, read_only=True)
    price = serializers.DecimalField(max_digits=6, decimal_places=2, read_only=True)
    quantity = serializers.IntegerField()  

    class Meta:
        model = Cart
        fields = ['user_id', 'menuitem_id', 'unit_price', 'price', 'quantity']  


class OrderSerializer(serializers.ModelSerializer): 
    user_id = serializers.IntegerField(read_only=True) 
    delivery_id = serializers.IntegerField(read_only=True) 
    status = serializers.BooleanField() 
    total = serializers.DecimalField(max_digits=6, decimal_places=2) 
    date = serializers.DateField()

    class Meta: 
        model = Order 
        fields = ['user_id', 'delivery_id', 'status', 'unit_price', 'price']

class OrderItemSerializer(serializers.ModelSerializer): 
    order_id = serializers.IntegerField(read_only=True)
    menuitem_id = serializers.IntegerField() 
    quantity = serializers.IntegerField() 
    unit_price = serializers.DecimalField(max_digits=6, decimal_places=2, read_only=True)
    price = serializers.DecimalField(max_digits=6, decimal_places=2, read_only=True)

    class Meta: 
        model = OrderItem 
        fields = ['order_id', 'menuitem_id', 'quantity', 'unit_price', 'price']