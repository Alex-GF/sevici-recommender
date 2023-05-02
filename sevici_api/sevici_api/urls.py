from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from data_manager.endpoints import StationStatusViewSet
from recommender.endpoints import bikes_predictors_regression


# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/stations/', StationStatusViewSet.as_view(), name='stations'),
    path('api/station/', bikes_predictors_regression, name='station'),
    path('api/admin/', admin.site.urls),
    path('api/api-auth/', include('rest_framework.urls')),
]
