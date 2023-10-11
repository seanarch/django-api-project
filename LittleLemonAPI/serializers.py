from rest_framework import serializers 
from .models import MenuItem, Category 

class CategorySerializer(serializers.ModelSerializer): 
    class Meta: 
        model = Category
        fields = ['id', 'title'] 

class MenuItemSerializer(serializers.ModelSerializer): 
    category_id = serializers.IntegerField()  

    class Meta: 
        model = MenuItem 
        fields = ['id', 'title', 'price',   'category_id', 'featured']

 