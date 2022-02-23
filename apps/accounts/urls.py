from django.urls import path, include

urlpatterns = [
    path('api/v1/', include('apps.accounts.api.v1.urls')),
    path('mvt/v1/', include('apps.accounts.mvt.v1.urls')),
]
