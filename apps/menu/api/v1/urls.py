from django.urls import path, include
from .views import CategoryListView, ProductListView, OrderItemListCreateView, OrderListCreateView, ProductDetailView, \
    OrderUpdateView, RemoveOrderItemView

urlpatterns = [
    path('category-list/', CategoryListView.as_view(), name='category-list'),
    path('product-list/', ProductListView.as_view(), name='product-list'),
    path('product-detail/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
    path('order-item-list-create/', OrderItemListCreateView.as_view(), name='order-item-list-create'),
    path('order-list-create/', OrderListCreateView.as_view(), name='order-list-create'),
    path('order-update/<int:pk>/', OrderUpdateView.as_view(), name='order-update'),
    path('remove-order-item/<int:pk>/', RemoveOrderItemView.as_view(), name='remove-order-item'),
]