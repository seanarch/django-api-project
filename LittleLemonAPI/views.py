from rest_framework import generics, status, serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from django.contrib.auth.models import User, Group
from .permissions import CanManageMenuItemPermission, DeliveryGroupPermission
from .models import MenuItem, Category, Cart, Order, OrderItem
from .serializers import MenuItemSerializer, CategorySerializer, UserSerializer, CartSerializer, OrderSerializer, OrderItemSerializer 
from decimal import Decimal 

 
class CategoriesView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    throttle_classes = [UserRateThrottle, AnonRateThrottle] 

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
    throttle_classes = [UserRateThrottle, AnonRateThrottle] 

class SingleMenuItemView(generics.RetrieveUpdateDestroyAPIView): 
    queryset = MenuItem.objects.all() 
    serializer_class = MenuItemSerializer  

    permission_classes = [CanManageMenuItemPermission]
    throttle_classes = [UserRateThrottle, AnonRateThrottle] 

class AssignUserToGroupView(generics.ListCreateAPIView):
    serializer_class = UserSerializer
    throttle_classes = [UserRateThrottle] 

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
    throttle_classes = [UserRateThrottle]

    def create(self, request, *args, **kwargs):
        return self.assign_user_to_group(request, 'manager')


class SingleManagerView(generics.RetrieveUpdateDestroyAPIView): 
    queryset = User.objects.filter(groups__name='manager')
    serializer_class = UserSerializer
    throttle_classes = [UserRateThrottle] 

    permission_classes = [CanManageMenuItemPermission]

class DeliveryUsersView(AssignUserToGroupView):
    queryset = User.objects.filter(groups__name='delivery')
    throttle_classes = [UserRateThrottle] 
    permission_classes = [DeliveryGroupPermission]

    def create(self, request, *args, **kwargs):
        return self.assign_user_to_group(request, 'delivery')
        

class SingleDeliveryUsersView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.filter(groups__name='delivery')
    serializer_class = UserSerializer
    throttle_classes = [UserRateThrottle] 
    permission_classes = [DeliveryGroupPermission]
 

class CartView(generics.ListCreateAPIView, generics.DestroyAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    throttle_classes = [UserRateThrottle, AnonRateThrottle]
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        menuitem_id = request.data.get('menuitem_id')
        if isinstance(menuitem_id, tuple):
            # If it's a tuple, access the first element (assuming it's the desired value)
            menuitem_id = menuitem_id[0]
        quantity = request.data.get('quantity', 1)  # Default to 1 if quantity is not provided

        if not request.user.is_authenticated:
            raise serializers.ValidationError("User must be authenticated to create a cart item")

        user = request.user

        try:
            menuitem = MenuItem.objects.get(pk=menuitem_id)
            unit_price = menuitem.price
            price = unit_price * Decimal(quantity)  # Calculate the price based on unit price and quantity
        except MenuItem.DoesNotExist:
            unit_price = 0
            price = 0

        cart_data = {
            'user_id': user.id,
            'menuitem_id': menuitem_id,
            'unit_price': unit_price,
            'price': price,
            'quantity': quantity,
        }

        cart_item = Cart.objects.create(**cart_data)

        # Return a response indicating the item was created successfully
        return Response(CartSerializer(cart_item).data, status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        # Handle DELETE request to delete all cart items created by the current user
        Cart.objects.filter(user=request.user).delete()
        return self.list(request, *args, **kwargs)

    def get_object(self):
        return Cart.objects.filter(user=self.request.user)
 

class OrderView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    throttle_classes = [UserRateThrottle, AnonRateThrottle]
    permission_classes = [IsAuthenticated, DeliveryGroupPermission]

    def create(self, request, *args, **kwargs):
        # Get the current user's cart items
        cart_items = Cart.objects.filter(user=request.user)

        if not cart_items.exists():
            return Response("Cart is empty.", status=status.HTTP_400_BAD_REQUEST)

        # Create a new order
        order = Order.objects.create(user=request.user)

        order_total = 0  # Initialize the order total

        # Add cart items to the order items table and calculate the total
        for cart_item in cart_items:
            order_item = OrderItem(
                order=order,
                menuitem=cart_item.menuitem,   
                quantity=cart_item.quantity,   
                unit_price=cart_item.unit_price,
                price=cart_item.price
            )
            order_item.save()

            # Calculate the subtotal for this order item and add it to the order total
            subtotal = cart_item.menuitem.price * cart_item.quantity  # Adjust this based on your model
            order_total += subtotal

        # Set the calculated order total
        order.total = order_total 
        order.save()

        # Delete all cart items
        cart_items.delete()

        # Serialize the created order and return the response
        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
class SingleOrderView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.filter()
    serializer_class = OrderSerializer
    throttle_classes = [UserRateThrottle] 

    permission_classes = [CanManageMenuItemPermission]    

 
