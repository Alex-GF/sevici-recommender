from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from data_manager.endpoints import StationStatusViewSet, StationStatusNearbyViewSet
from recommender.endpoints import bikes_predictors_regression, bikes_predictors_mean, station_predictors_nearby
from django.conf.urls.static import static
from swagger_render.views import SwaggerUIView

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()

urlpatterns = [
    path('api', include(router.urls)),
    path('api/stations/all', StationStatusViewSet.as_view(), name='stations_all'),
    path('api/stations/nearby', StationStatusNearbyViewSet.as_view(), name="stations_nearby"),
    path('api/predictors/linear', bikes_predictors_regression, name='station'),
    path('api/predictors/mean', bikes_predictors_mean, name='predictor_mean'),
    path('api/predictors/nearby', station_predictors_nearby, name='predictor_nearby'),
    path('api/admin/', admin.site.urls),
    path('api/api-auth/', include('rest_framework.urls')),
    path('api/docs', SwaggerUIView.as_view()),
] + static('/docs/', document_root='docs')