from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from import_export.admin import ImportExportActionModelAdmin, ImportExportModelAdmin

from .models import Category, Meal, Order, OrderItem
from .export import ProductExport


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'is_active', 'created_at')
    list_filter = ('created_at', 'is_active')
    search_fields = ('title', )


class MealAdmin(admin.ModelAdmin):
    list_display = ('id', 'category', 'title', 'image_tag', 'cost', 'is_active', 'created_at')
    list_filter = ('created_at', 'is_active', 'category')
    search_fields = ('title', 'category__title')


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    fk_name = 'order'
    fields = ('id', 'meal', 'price', 'quantity', 'total', 'is_completed', 'updated_at', 'created_at')
    readonly_fields = ('id', 'created_at', 'updated_at', 'total', 'price')
    extra = 1
    
    def has_change_permission(self, request, obj=None):
        return False

    # def has_add_permission(self, request, obj):
    #     return False
    #
    # def has_change_permission(self, request, obj=None):
    #     return False
    #
    # def has_delete_permission(self, request, obj=None):
    #     return False


class OrderAdmin(ImportExportModelAdmin, ImportExportActionModelAdmin, admin.ModelAdmin):
    inlines = (OrderItemInline,)
    list_display = ('id', 'waiter', 'table', 'get_cart_total', 'get_cart_items', 'status', 'payed', 'updated_at', 'created_at')
    list_filter = ('created_at', 'status', 'waiter')
    search_fields = ('waiter__first_name', 'waiter__last_name', 'id')
    readonly_fields = ('get_cart_total', 'created_at', 'waiter', 'updated_at', 'get_cart_items',)
    date_hierarchy = 'created_at'
    resource_class = ProductExport
    fieldsets = (
        (_('Order information'), {'fields': ('waiter', 'table', 'get_cart_total', 'get_cart_items', 'status', 'payed',
                                             'updated_at', 'created_at')}),
        # (_('Order Items'), {'fields': (inlines, )}),

    )

    def save_model(self, request, obj, form, change):
        obj.waiter = request.user
        super().save_model(request, obj, form, change)

    # def render_change_form(self, request, context, add=False, change=False, form_url='', obj=None):
    #     context.update({
    #         'show_save': False,
    #         'show_save_and_continue': False,
    #         'show_save_and_add_another': False,
    #         'show_delete': False
    #     })
    #     return super().render_change_form(request, context, add, change, form_url, obj)

    # def has_add_permission(self, request):
    #     return False
    #
    # def has_change_permission(self, request, obj=None):
    #     return False
    #
    # def has_delete_permission(self, request, obj=None):
    #     return False


admin.site.register(Category, CategoryAdmin)
admin.site.register(Meal, MealAdmin)
admin.site.register(Order, OrderAdmin)
