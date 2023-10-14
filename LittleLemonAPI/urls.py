from django.urls import path 
from . import views

urlpatterns = [
    path('category', views.CategoriesView.as_view()), 
    path('menu-items', views.MenuItemsView.as_view()),
    # path('category/<int:pk>', views.SingleCateItemView.as_view()), 
    path('menu-items/<int:pk>', views.SingleMenuItemView.as_view()), 
    path('groups/manager/users', views.ManagerUsersView.as_view()), 
    path('groups/manager/users/<int:pk>', views.SingleManagerView.as_view()),
    path('groups/delivery-crew/users', views.DeliveryUsersView.as_view()),
    path('groups/delivery-crew/users/<int:pk>', views.SingleDeliveryUsersView.as_view()),
    path('cart/menu-items', views.CartView.as_view())
]