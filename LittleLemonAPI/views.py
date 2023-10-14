from rest_framework import generics, status
from rest_framework.response import Response
from django.contrib.auth.models import User, Group
from .permissions import CanManageMenuItemPermission, DeliveryGroupPermission
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

class SingleMenuItemView(generics.RetrieveUpdateDestroyAPIView): 
    queryset = MenuItem.objects.all() 
    serializer_class = MenuItemSerializer  

    permission_classes = [CanManageMenuItemPermission]


class ManagerUsersView(generics.ListCreateAPIView):
    queryset = User.objects.filter(groups__name='manager')
    serializer_class = UserSerializer
    permission_classes = [CanManageMenuItemPermission]

    def create(self, request, *args, **kwargs):
        username = request.data.get('username')

        try:
            user = User.objects.get(username=username)
            manager_group, _ = Group.objects.get_or_create(name='manager')
            user.groups.add(manager_group)

            # Serialize the user data
            user_serializer = UserSerializer(user)

            return Response(user_serializer.data, status=status.HTTP_201_CREATED)
        except User.DoesNotExist:
            return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)


class SingleManagerView(generics.RetrieveUpdateDestroyAPIView): 
    queryset = User.objects.filter(groups__name='manager')
    serializer_class = UserSerializer

    permission_classes = [CanManageMenuItemPermission]

class DeliveryUsersView(generics.ListCreateAPIView):
    queryset = User.objects.filter(groups__name='delivery')
    serializer_class = UserSerializer
    permission_classes = [DeliveryGroupPermission]

    def create(self, request, *args, **kwargs): 
        username = request.data.get('username') 

        try:
            user = User.objects.get(username=username)
            manager_group, _ = Group.objects.get_or_create(name='delivery')
            user.groups.add(manager_group)

            # Serialize the user data
            user_serializer = UserSerializer(user)

            return Response(user_serializer.data, status=status.HTTP_201_CREATED)
        except User.DoesNotExist:
            return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        
        
class SingleDeliveryUsersView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.filter(groups__name='delivery')
    serializer_class = UserSerializer

    permission_classes = [DeliveryGroupPermission]