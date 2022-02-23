from datetime import datetime

from django.db.models import Q
from rest_framework import generics, status
from rest_framework.response import Response

from apps.menu.models import Category, Meal, Order, OrderItem
from .serializers import CategorySerializer, MealSerializer, OrderListSerializer, OrderCreateSerializer, OrderItemSerializer


class CategoryListView(generics.ListAPIView):
    # http://127.0.0.1:8000/menu/api/v1/category-list/
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
    # http://127.0.0.1:8000/menu/api/v1/product-list/
    serializer_class = MealSerializer

    def get_queryset(self):
        cat = self.request.GET.get('cat')
        cat_condition = Q()
        if cat:
            cat_condition = Q(category_id=cat)
        queryset = Meal.objects.filter(cat_condition, is_active=True)
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if queryset:
            serializer = self.get_serializer(queryset, many=True)
            return Response({'success': True, 'data': serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({'success': False, 'data': 'queryset did not match'}, status=status.HTTP_404_NOT_FOUND)


class ProductDetailView(generics.RetrieveAPIView):
    # http://127.0.0.1:8000/menu/api/v1/product-detail/<id>/
    serializer_class = MealSerializer
    queryset = Meal.objects.all()

    def get(self, request, *args, **kwargs):
        queryset = self.get_object()
        if queryset:
            serializer = self.get_serializer(queryset)
            return Response({'success': True, 'data': serializer.data}, status=status.HTTP_200_OK)
        return Response({'success': False, 'data': 'queryset did not match'}, status=status.HTTP_404_NOT_FOUND)


class OrderItemListCreateView(generics.ListCreateAPIView):
    # http://127.0.0.1:8000/menu/api/v1/order-item-list-create/
    serializer_class = OrderItemSerializer
    queryset = OrderItem.objects.all()

    def get_queryset(self):
        order = self.request.GET.get('order')
        user = self.request.GET.get('user')
        order_condition = Q()
        if order:
            order_condition = Q(order_id=order)
        user_condition = Q()
        if user:
            user_condition = Q()
        queryset = OrderItem.objects.filter(order_condition)
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if queryset:
            serializer = self.get_serializer(queryset, many=True)
            return Response({'success': True, 'data': serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({'success': False, 'data': 'queryset did not match'}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'success': True, 'data': serializer.data}, status=status.HTTP_201_CREATED)
        else:
            return Response({'success': False, 'message': 'Credentials is invalid'}, status=status.HTTP_400_BAD_REQUEST)


class OrderListCreateView(generics.ListCreateAPIView):
    # http://127.0.0.1:8000/menu/api/v1/order-list-create/
    queryset = Order.objects.all()

    def get_queryset(self):
        waiter = self.request.GET.get('waiter')
        waiter_condition = Q()
        today = datetime.now().date()
        print(today)
        if waiter:
            waiter_condition = Q(waiter_id=waiter)
        queryset = Order.objects.filter(waiter_condition & Q(updated_at__date=today))
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset().order_by('-updated_at')
        if queryset:
            serializer = OrderListSerializer(queryset, many=True)
            return Response({'success': True, 'data': serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({'success': False, 'data': 'queryset did not match'}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request, *args, **kwargs):
        try:
            order = Order.objects.create(waiter_id=request.data['waiter'], table=request.data['table'])
        except Exception as e:
            return Response({'success': False, 'data': f'{e.args}'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            if request.data['order_items']:
                for item in request.data['order_items']:
                    meal = Meal.objects.get(id=item['meal'])
                    quantity = item['quantity']
                    OrderItem.objects.create(meal=meal, quantity=quantity, order=order)

                serializer = OrderCreateSerializer(instance=order)
                return Response({'success': True, 'data': serializer.data}, status=status.HTTP_201_CREATED)
            else:
                return Response({'success': False, 'data': 'Order Items not found'}, status=status.HTTP_400_BAD_REQUEST)


class OrderUpdateView(generics.CreateAPIView):
    # http://127.0.0.1:8000/menu/api/v1/order-update/<order_id>/
    serializer_class = OrderCreateSerializer
    queryset = Order.objects.all()

    def post(self, request, *args, **kwargs):
        obj = self.get_object()
        for item in request.data:
            meal = Meal.objects.get(id=item['meal'])
            quantity = item['quantity']
            OrderItem.objects.create(meal=meal, quantity=quantity, order=obj)
        obj.status = 1
        obj.save()
        serializer = OrderCreateSerializer(instance=obj)
        return Response({'success': True, 'data': serializer.data}, status=status.HTTP_201_CREATED)


class RemoveOrderItemView(generics.DestroyAPIView):
    # http://127.0.0.1:8000/menu/api/v1/remove-order-item/<order_id>/?order_item_id=<id>
    serializer_class = OrderCreateSerializer
    queryset = Order.objects.all()

    def delete(self, request, *args, **kwargs):
        order_item_id = request.GET.get('order_item_id')
        order = self.get_object()
        try:
            order_item = OrderItem.objects.get(id=order_item_id)
        except Exception as e:
            return Response({'success': False, 'data': f'{e.args}'}, status=status.HTTP_406_NOT_ACCEPTABLE)
        else:
            order_item.delete()
            data = 'Successfully deleted'
            order_item_count = order.order_items.all().count()
            if order_item_count == 0:
                order.delete()
            return Response({'success': True, 'data': data}, status=status.HTTP_200_OK)


