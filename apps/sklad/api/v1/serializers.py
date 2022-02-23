from rest_framework import serializers

from apps.sklad.models import Category, Product, ProductOrder


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('id', 'title', 'is_active', 'created_at')


class ProductSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.title', read_only=True)

    class Meta:
        model = Product
        fields = ('id', 'category', 'category_name', 'title', 'unit', 'is_active', 'created_at')


class ProductOrderSerializer(serializers.ModelSerializer):
    supplier_name = serializers.CharField(source='supplier.get_full_name', read_only=True)
    category_name = serializers.CharField(source='category.title', read_only=True)
    product_name = serializers.CharField(source='product.title', read_only=True)
    product_unit_id = serializers.CharField(source='product.unit', read_only=True)
    product_unit = serializers.SerializerMethodField(read_only=True)

    def get_product_unit(self, obj):
        return obj.product.get_unit_display()

    class Meta:
        model = ProductOrder
        fields = ('id', 'supplier', 'supplier_name', 'category', 'category_name', 'product', 'product_name',
                  'price', 'product_unit_id', 'product_unit', 'quantity', 'created_at')
