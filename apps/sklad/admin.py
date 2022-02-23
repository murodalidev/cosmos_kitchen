from django.contrib import admin
from import_export.admin import ImportExportActionModelAdmin, ImportExportModelAdmin
from .models import Category, Product, ProductOrder, UsedProduct
from .export import ProductExport, ProductInExport, ProductOutExport


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'is_active', 'created_at')
    list_filter = ('created_at', 'is_active')
    search_fields = ('title', )


class ProductAdmin(ImportExportModelAdmin, ImportExportActionModelAdmin, admin.ModelAdmin):
    list_display = ('id', 'category', 'title', 'quantity', 'unit', 'is_active', 'created_at')
    list_filter = ('created_at', 'is_active', 'category')
    search_fields = ('title', 'category__title')
    
    resource_class = ProductExport


class ProductOrderAdmin(ImportExportModelAdmin, ImportExportActionModelAdmin, admin.ModelAdmin):
    list_display = ('id', 'supplier', 'category', 'product', 'get_unit', 'quantity', 'price', 'created_at')
    autocomplete_fields = ('category', 'product')
    list_filter = ('created_at', )
    readonly_fields = ('category', 'supplier')
    search_fields = ('supplier__first_name', 'supplier__last_name', 'category__title', 'product__title')
    resource_class = ProductInExport

    def save_model(self, request, obj, form, change):
        obj.supplier = request.user
        obj.category = obj.product.category
        super().save_model(request, obj, form, change)

    def get_unit(self, obj):
        return obj.product.get_unit_display()


class UsedProductAdmin(ImportExportModelAdmin, ImportExportActionModelAdmin, admin.ModelAdmin):
    list_display = ('id', 'chef', 'category', 'product', 'get_unit', 'quantity', 'created_at')
    autocomplete_fields = ('category', 'product')
    list_filter = ('created_at', )
    readonly_fields = ('category', 'chef')
    search_fields = ('chef__first_name', 'chef__last_name', 'category__title', 'product__title')

    def get_unit(self, obj):
        return obj.product.get_unit_display()
    
    def save_model(self, request, obj, form, change):
        obj.chef = request.user
        super().save_model(request, obj, form, change)

    resource_class = ProductOutExport


admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductOrder, ProductOrderAdmin)
admin.site.register(UsedProduct, UsedProductAdmin)