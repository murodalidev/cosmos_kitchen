from django.urls import path, include
from .views import AccountListView, AccountVerifyView

urlpatterns = [
    path('list/', AccountListView.as_view(), name='account-list'),
    path('verify/<int:telegram_id>/', AccountVerifyView.as_view(), name='account-verify'),
]
