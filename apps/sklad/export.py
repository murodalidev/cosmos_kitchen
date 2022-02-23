from import_export import resources
from import_export.fields import Field
from . import models


class ProductExport(resources.ModelResource):
    category = Field(attribute='category__title', column_name="Kategoriya")
    title = Field(attribute='title', column_name="Mahsulot")
    quantity = Field(attribute='quantity', column_name="Miqdori")
    get_unit = Field(attribute='get_unit_display', column_name="Birligi")
    created_at = Field(attribute='created_at__date', column_name="Sana")

    class Meta:
        model = models.Product
        fields = [
            'category', 'title', 'quantity', 'get_unit', 'created_at'
        ]


class ProductInExport(resources.ModelResource):
    supplier = Field(attribute='supplier__get_full_name', column_name='Ta\'minotchi')
    category = Field(attribute='category__title', column_name="Kategoriya")
    product = Field(attribute='product__title', column_name="Mahsulot")
    quantity = Field(attribute='quantity', column_name="Miqdori")
    get_unit = Field(attribute='product__get_unit_display', column_name="Birligi")
    price = Field(attribute='price', column_name="Narxi")
    created_at = Field(attribute='created_at__date', column_name="Sana")

    class Meta:
        model = models.Product
        fields = [
            'supplier', 'category', 'product', 'quantity', 'get_unit', 'price', 'created_at'
        ]

class ProductOutExport(resources.ModelResource):
    chef = Field(attribute='chef__get_full_name', column_name='Ta\'minotchi')
    category = Field(attribute='category__title', column_name="Kategoriya")
    product = Field(attribute='product__title', column_name="Mahsulot")
    quantity = Field(attribute='quantity', column_name="Miqdori")
    get_unit = Field(attribute='product__get_unit_display', column_name="Birligi")
    created_at = Field(attribute='created_at__date', column_name="Sana")

    class Meta:
        model = models.Product
        fields = [
            'chef', 'category', 'product', 'quantity', 'get_unit', 'created_at'
        ]