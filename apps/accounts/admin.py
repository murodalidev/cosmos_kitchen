from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Account
from .forms import AccountCreationForm, AccountChangeForm


class AccountAdmin(BaseUserAdmin):
    form = AccountChangeForm
    add_form = AccountCreationForm
    list_display = ('id', 'first_name', 'last_name', 'phone', 'telegram_id', 'role',
                    'is_superuser', 'is_staff', 'is_active', 'updated_at', 'created_at')
    readonly_fields = ('updated_at', 'created_at', 'is_superuser',)
    list_filter = ('created_at', 'role', 'is_superuser', 'is_staff', 'is_active')
    ordering = ('-id',)
    fieldsets = (
        (_('Personal information'), {'fields': ('phone', 'email', ('first_name', 'last_name'), 'telegram_id',
                                                'password')}),
        (_('Permissions'), {'fields': ('role', 'is_superuser', 'is_staff', 'is_active',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('updated_at', 'created_at')}),
    )
    add_fieldsets = (
        ('Personal information', {'classes': ('wide',),
                                  'fields': (('phone', 'telegram_id'), ('first_name', 'last_name'), 'email',
                                             ('password1', 'password2'))}),
    )
    search_fields = ('phone', 'first_name', 'last_name')


admin.site.register(Account, AccountAdmin)

admin.site.site_header = "APART HOTEL COSMOS"
admin.site.site_title = "APART HOTEL COSMOS"
admin.site.index_title = "Welcome to APART HOTEL COSMOS Food Portal"
