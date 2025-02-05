from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CountryViewSet, CityViewSet, AirportViewSet

router = DefaultRouter()
router.register(r'countries', CountryViewSet, basename='countries')
router.register(r'cities', CityViewSet, basename='cities')
router.register(r'airports', AirportViewSet, basename='airports')

urlpatterns = [
    path('', include(router.urls)),
] 