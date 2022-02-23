from django.db.models import Q
from rest_framework import generics, status
from rest_framework.response import Response

from apps.sklad.models import Category, Product, ProductOrder
from apps.accounts.models import Account
from .serializers import CategorySerializer, ProductSerializer, ProductOrderSerializer


class CategoryListView(generics.ListAPIView):
    # http://127.0.0.1:8000/sklad/api/v1/category-list/
    serializer_class = CategorySerializer

    def get_queryset(self):
        queryset = Category.objects.filter(is_active=True)
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if queryset:
            serializer = self.get_serializer(queryset, many=True)
            return Response({'success': True, 'data': serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({'success': False, 'data': 'queryset did not match'}, status=status.HTTP_404_NOT_FOUND)


class ProductListView(generics.ListAPIView):
    # http://127.0.0.1:8000/sklad/api/v1/product-list/
    serializer_class = ProductSerializer

    def get_queryset(self):
        cat = self.request.GET.get('cat')
        cat_condition = Q()
        if cat:
            cat_condition = Q(category_id=cat)
        queryset = Product.objects.filter(cat_condition, is_active=True)
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if queryset:
            serializer = self.get_serializer(queryset, many=True)
            return Response({'success': True, 'data': serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({'success': False, 'data': 'queryset did not match'}, status=status.HTTP_404_NOT_FOUND)


class ProductDetailView(generics.RetrieveAPIView):
    # http://127.0.0.1:8000/sklad/api/v1/product-detail/<product_id>/
    serializer_class = ProductSerializer
    queryset = Product.objects.all()

    def get(self, request, *args, **kwargs):
        queryset = self.get_object()
        if queryset:
            serializer = self.get_serializer(queryset)
            return Response({'success': True, 'data': serializer.data}, status=status.HTTP_200_OK)
        return Response({'success': False, 'data': 'queryset did not match'}, status=status.HTTP_404_NOT_FOUND)



class ProductOrderCreateView(generics.CreateAPIView):
    # http://127.0.0.1:8000/sklad/api/v1/order-create/
    serializer_class = ProductOrderSerializer
    queryset = ProductOrder.objects.all()

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'success': True, 'data': serializer.data}, status=status.HTTP_201_CREATED)
        else:
            return Response({'success': False, 'message': 'Credentials is invalid'}, status=status.HTTP_400_BAD_REQUEST)
