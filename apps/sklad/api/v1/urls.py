from django.urls import path, include
from .views import CategoryListView, ProductListView, ProductOrderCreateView, ProductDetailView

urlpatterns = [
    path('category-list/', CategoryListView.as_view(), name='category-list'),
    path('product-list/', ProductListView.as_view(), name='product-list'),
    path('product-detail/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
    path('order-create/', ProductOrderCreateView.as_view(), name='order-create'),
]