from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth.models import User, Group
from .permissions import CanManageMenuItemPermission, DeliveryGroupPermission
from .models import MenuItem, Category, Cart
from .serializers import MenuItemSerializer, CategorySerializer, UserSerializer, CartSerializer 

 
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

class AssignUserToGroupView(generics.ListCreateAPIView):
    serializer_class = UserSerializer

    def assign_user_to_group(self, request, group_name):
        username = request.data.get('username')

        try:
            user = User.objects.get(username=username)
            group, _ = Group.objects.get_or_create(name=group_name)
            user.groups.add(group)

            user_serializer = UserSerializer(user)
            return Response(user_serializer.data, status=status.HTTP_201_CREATED)

        except User.DoesNotExist:
            return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

class ManagerUsersView(AssignUserToGroupView):
    queryset = User.objects.filter(groups__name='manager')
    permission_classes = [CanManageMenuItemPermission]

    def create(self, request, *args, **kwargs):
        return self.assign_user_to_group(request, 'manager')


class SingleManagerView(generics.RetrieveUpdateDestroyAPIView): 
    queryset = User.objects.filter(groups__name='manager')
    serializer_class = UserSerializer

    permission_classes = [CanManageMenuItemPermission]

class DeliveryUsersView(AssignUserToGroupView):
    queryset = User.objects.filter(groups__name='delivery')
    permission_classes = [DeliveryGroupPermission]

    def create(self, request, *args, **kwargs):
        return self.assign_user_to_group(request, 'delivery')
        

class SingleDeliveryUsersView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.filter(groups__name='delivery')
    serializer_class = UserSerializer

    permission_classes = [DeliveryGroupPermission]

class CartView(generics.ListCreateAPIView, generics.DestroyAPIView): 
    queryset = Cart.objects.all() 
    serializer_class = CartSerializer 
    permission_classes = [IsAuthenticated] 

    def destroy(self, request, *args, **kwargs):
        # Handle DELETE request to delete all cart items created by the current user
        Cart.objects.filter(user=request.user).delete()
        return self.list(request, *args, **kwargs)

    def get_object(self):
        return Cart.objects.filter(user=self.request.user)