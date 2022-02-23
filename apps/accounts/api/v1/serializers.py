from rest_framework import serializers
from apps.accounts.models import Account


class AccountSerializer(serializers.ModelSerializer):
    role_name = serializers.SerializerMethodField(read_only=True)

    def get_role_name(self, obj):
        return obj.get_role_display()

    class Meta:
        model = Account
        fields = ('id', 'get_full_name', 'phone', 'telegram_id', 'role', 'role_name')
