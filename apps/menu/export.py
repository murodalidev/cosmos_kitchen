from import_export import resources
from import_export.fields import Field
from . import models


class ProductExport(resources.ModelResource):
    waiter = Field(attribute='waiter__get_full_name', column_name="Waiter")
    table = Field(attribute='table', column_name="Table")
    status = Field(attribute='get_status_display', column_name="Status")
    items = Field(attribute='get_cart_items', column_name='Items')
    total = Field(attribute='get_cart_total', column_name='Total')
    created_at = Field(attribute='created_at__date', column_name="Created at")

    class Meta:
        model = models.Order
        fields = [
            'waiter', 'table', 'status', 'items', 'total', 'created_at'
        ]