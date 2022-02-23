"""kitchen URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from apps.menu.mvt.v1.views import order_list, complete_order, cancel_order, pending_order, payment_type
from apps.menu.mvt.v1.check import print_check

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', order_list, name='order-list-view'),
    path('complete/', complete_order, name='complete-order'),
    path('cancel/', cancel_order, name='cancel-order'),
    path('pending/', pending_order, name='pending-order'),
    path('payment_type/', payment_type, name='payment_type'),
    path('print_check/<int:pk>/', print_check, name='print-check'),

    path('account/', include('apps.accounts.urls')),
    path('menu/', include('apps.menu.urls')),
    path('sklad/', include('apps.sklad.urls')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
