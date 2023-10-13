from django.urls import path 
from . import views

urlpatterns = [
    path('category', views.CategoriesView.as_view()), 
    path('menu-items', views.MenuItemsView.as_view()),
    path('category/<int:pk>', views.SingleCateItemView.as_view()), 
]