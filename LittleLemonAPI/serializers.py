from rest_framework import serializers 
from .models import MenuItem, Category, Cart  
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
    price = serializers.DecimalField(max_digits=6, decimal_places=2, read_only=True)  # Add price field

    class Meta:
        model = Cart
        fields = ['user_id', 'menuitem_id', 'unit_price', 'price']

    def create(self, validated_data): 
        menuitem_id = validated_data.get('menuitem_id')
        quantity = validated_data.get('quantity', 1)  # Default to 1 if quantity is not provided

        request = self.context.get("request")

        if request and request.user.is_authenticated: 
            user = request.user
            validated_data['user_id'] = user.id 
            try:
                menuitem = MenuItem.objects.get(pk=menuitem_id)
                unit_price = menuitem.price
                price = unit_price * quantity  # Calculate the price based on unit price and quantity
            except MenuItem.DoesNotExist:
                unit_price = 0
                price = 0

            validated_data['unit_price'] = unit_price
            validated_data['price'] = price

            return super(CartSerializer, self).create(validated_data)
        else: 
            raise serializers.ValidationError("User must be authenticated to create a cart item")

 