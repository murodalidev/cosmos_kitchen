from django.urls import path, include

urlpatterns = [
    path('api/v1/', include('apps.menu.api.v1.urls')),
    path('v1/', include('apps.menu.mvt.v1.urls')),
]
