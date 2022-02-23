from django.db.models import Q
from rest_framework import generics, status
from rest_framework.response import Response
from django.contrib.auth import authenticate, login

from apps.accounts.models import Account
from .serializers import AccountSerializer


class AccountListView(generics.ListAPIView):
    # http://127.0.0.1:8000/account/api/v1/list/
    serializer_class = AccountSerializer

    def get_queryset(self):
        tg = self.request.GET.get('telegram_id')
        phone = self.request.GET.get('phone')

        tg_condition = Q()
        if tg:
            tg_condition = (Q(telegram_id=tg))
        phone_condition = Q()
        if phone:
            phone_condition = Q(phone=phone)

        queryset = Account.objects.filter(tg_condition, phone_condition)

        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if queryset:
            serializer = self.get_serializer(queryset, many=True)
            return Response({'success': True, 'data': serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({'success': False, 'data': 'queryset did not match'}, status=status.HTTP_404_NOT_FOUND)


class AccountVerifyView(generics.RetrieveAPIView):
    # http://127.0.0.1:8000/account/api/v1/verify/<telegram_id>/
    serializer_class = AccountSerializer
    lookup_field = 'telegram_id'

    def get(self, request, telegram_id=None, *args, **kwargs):
        try:
            account = Account.objects.get(telegram_id=telegram_id)
        except Exception as e:
            return Response({'success': False, 'data': {'error': f'{e}'}}, status=status.HTTP_404_NOT_FOUND)
        else:
            serializer = self.get_serializer(account)
            return Response({'success': True, 'data': serializer.data}, status=status.HTTP_200_OK)