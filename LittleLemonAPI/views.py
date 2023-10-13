from rest_framework import generics
from django.contrib.auth.models import User
from .permissions import CanManageMenuItemPermission
from .models import MenuItem, Category
from .serializers import MenuItemSerializer, CategorySerializer, UserSerializer

 
class CategoriesView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class MenuItemsView(generics.ListCreateAPIView): 
    queryset = MenuItem.objects.all() 
    serializer_class = MenuItemSerializer
    ordering_fields = ['price'] 
    # filterset_fields = [] 
    # search_fields = [] 

    def get_queryset(self):
        queryset = MenuItem.objects.all()
        category = self.request.query_params.get('category', None)
        if category:
            queryset = queryset.filter(category=category)
        return queryset
    
    permission_classes = [CanManageMenuItemPermission]

# class SingleCateItemView(generics.RetrieveUpdateDestroyAPIView): 
#     queryset = Category.objects.all() 
#     serializer_class = CategorySerializer     

class SingleMenuItemView(generics.RetrieveUpdateDestroyAPIView): 
    queryset = MenuItem.objects.all() 
    serializer_class = MenuItemSerializer  

    permission_classes = [CanManageMenuItemPermission]

class ManagerUsersView(generics.ListCreateAPIView):
    queryset = User.objects.filter(groups__name='manager')
    serializer_class = UserSerializer

class DeliveryUsersView(generics.ListCreateAPIView):
    queryset = User.objects.filter(groups__name='delivery')
    serializer_class = UserSerializer