from rest_framework import serializers

from apps.menu.models import Category, Meal, Order, OrderItem


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('id', 'title', 'is_active', 'created_at')


class MealSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.title', read_only=True)

    class Meta:
        model = Meal
        fields = ('id', 'category', 'category_name', 'title', 'get_image_url', 'cost', 'is_active', 'created_at')


class OrderItemSerializer(serializers.ModelSerializer):
    meal_name = serializers.CharField(source='meal.title', read_only=True)
    order_name = serializers.CharField(source='order.__str__', read_only=True)

    class Meta:
        model = OrderItem
        fields = ('id', 'meal', 'meal_name', 'order', 'order_name', 'quantity', 'is_completed', 'get_total',
                  'updated_at', 'created_at')


class OrderListSerializer(serializers.ModelSerializer):
    waiter_name = serializers.CharField(source='waiter.get_full_name',  read_only=True)
    order_items = serializers.SerializerMethodField(read_only=True)
    status_name = serializers.SerializerMethodField(read_only=True)

    def get_status_name(self, obj):
        return obj.get_status_display()

    def get_order_items(self, obj):
        queryset = OrderItem.objects.filter(order_id=obj.id)
        serializer = OrderItemSerializer(instance=queryset, many=True)
        return serializer.data

    class Meta:
        model = Order
        fields = ('id', 'waiter', 'table', 'waiter_name', 'get_cart_total', 'get_cart_items', 'order_items', 'status',
                  'status_name', 'updated_at', 'created_at')


class OrderItemMangerSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ('meal', 'quantity')


class OrderCreateSerializer(serializers.ModelSerializer):
    order_items = OrderItemMangerSerializer(many=True, read_only=True)
    status_name = serializers.SerializerMethodField(read_only=True)

    def get_status_name(self, obj):
        return obj.get_status_display()

    class Meta:
        model = Order
        fields = ('id', 'status', 'status_name', 'waiter', 'table', 'updated_at', 'created_at', 'order_items')



