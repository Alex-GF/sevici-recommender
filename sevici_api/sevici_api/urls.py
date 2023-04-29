from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from data_manager.endpoints import UserViewSet, StationStatusViewSet

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'stationsStatus', StationStatusViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/admin/', admin.site.urls),
    path('api/api-auth/', include('rest_framework.urls')),
]
