from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, BasePermission
from .models import MenuItem, Category
from .serializers import MenuItemSerializer, CategorySerializer

class CanPostMenuItemPermission(BasePermission): 
    def has_permission(self, request, view): 
        return request.user.groups.filter(name='manager').exists()
    
class CanPostCategoryPermission(BasePermission): 
    def has_object_permission(self, request, view, obj):
        return request.user.groups.filter(name='manager').exists() 
 
class CategoriesView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    permission_classes = [IsAuthenticated, CanPostMenuItemPermission]

class MenuItemsView(generics.ListCreateAPIView): 
    queryset = MenuItem.objects.all() 
    serializer_class = MenuItemSerializer
    ordering_fields = ['price'] 
    # filterset_fields = [] 
    # search_fields = [] 

    permission_classes = [IsAuthenticated, CanPostMenuItemPermission]

class SingleCateItemView(generics.RetrieveUpdateDestroyAPIView): 
    queryset = Category.objects.all() 
    serializer_class = CategorySerializer     

    permission_classes = [IsAuthenticated, CanPostMenuItemPermission]
 