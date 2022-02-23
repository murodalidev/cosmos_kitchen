from django.urls import path, include

urlpatterns = [
    path('api/v1/', include('apps.sklad.api.v1.urls')),
    path('mvt/v1/', include('apps.sklad.mvt.v1.urls')),
]
