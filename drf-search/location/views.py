from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Sum, F
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import Country, City, Airport
from .serializers import (
    CountrySerializer, CitySerializer, AirportSerializer,
    CountrySearchRatioSerializer, CountryCitySearchSerializer,
    MostSearchedCitiesSerializer
)

# Create your views here.

class BaseLocationViewSet(viewsets.ModelViewSet):
    def get_cookie_key(self):
        return f'selected_{self.basename}'

    @swagger_auto_schema(
        operation_description="Select a location and store it in cookies",
        responses={
            200: openapi.Response(
                description="Location selected successfully",
                examples={
                    "application/json": {
                        "status": "Location selected"
                    }
                }
            )
        }
    )
    @action(detail=True, methods=['post'])
    def select(self, request, pk=None):
        instance = self.get_object()
        response = Response({'status': 'Location selected'})
        
        # Set cookie for selected location
        response.set_cookie(
            self.get_cookie_key(),
            pk,
            max_age=86400,  # 24 hours
            httponly=True
        )
        
        # Increment search count
        instance.increment_search_count()
        
        return response

    @swagger_auto_schema(
        operation_description="Deselect the currently selected location",
        responses={
            200: openapi.Response(
                description="Location deselected successfully",
                examples={
                    "application/json": {
                        "status": "Location deselected"
                    }
                }
            )
        }
    )
    @action(detail=False, methods=['post'])
    def deselect(self, request):
        response = Response({'status': 'Location deselected'})
        response.delete_cookie(self.get_cookie_key())
        return response

    @swagger_auto_schema(
        operation_description="Search locations",
        manual_parameters=[
            openapi.Parameter(
                'q',
                openapi.IN_QUERY,
                description="Search query string",
                type=openapi.TYPE_STRING,
                required=True
            )
        ],
        responses={
            200: openapi.Response(description="Search results")
        }
    )
    @action(detail=False, methods=['get'])
    def search(self, request):
        query = request.query_params.get('q', '')
        queryset = self.get_queryset().search(query)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class CountryViewSet(BaseLocationViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    basename = 'countries'

    @swagger_auto_schema(
        operation_description="Get most searched cities for specified countries",
        manual_parameters=[
            openapi.Parameter(
                'country_code',
                openapi.IN_QUERY,
                description="Country codes (comma-separated)",
                type=openapi.TYPE_STRING,
                required=True,
                example="TR,UK"
            )
        ],
        responses={
            200: MostSearchedCitiesSerializer(many=True),
            400: "Bad Request - country_code is required"
        }
    )
    @action(detail=False, methods=['get'])
    def most_searched_cities(self, request):
        country_codes = request.query_params.get('country_code', '').split(',')
        country_codes = [code.strip() for code in country_codes if code.strip()]

        if not country_codes:
            return Response(
                {'error': 'country_code parameter is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        countries = Country.objects.filter(code__in=country_codes)
        serializer = MostSearchedCitiesSerializer(countries, many=True)
        
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Get search ratio statistics for specified countries",
        manual_parameters=[
            openapi.Parameter(
                'country_code',
                openapi.IN_QUERY,
                description="Country codes (comma-separated)",
                type=openapi.TYPE_STRING,
                required=True,
                example="TR,UK"
            )
        ],
        responses={
            200: CountrySearchRatioSerializer(many=True),
            400: "Bad Request - country_code is required"
        }
    )
    @action(detail=False, methods=['get'])
    def search_ratio(self, request):
        country_codes = request.query_params.get('country_code', '').split(',')
        country_codes = [code.strip() for code in country_codes if code.strip()]

        if not country_codes:
            return Response(
                {'error': 'country_code parameter is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        countries = Country.objects.filter(code__in=country_codes)
        result = []

        for country in countries:
            total_city_searches = country.cities.aggregate(
                total=Sum('search_count'))['total'] or 0
            total_airport_searches = country.airports.aggregate(
                total=Sum('search_count'))['total'] or 0
            
            search_ratio = (
                total_city_searches / total_airport_searches 
                if total_airport_searches > 0 else 0
            )

            data = {
                'code': country.code,
                'name': country.name,
                'search_ratio': round(search_ratio, 2),
                'total_city_searches': total_city_searches,
                'total_airport_searches': total_airport_searches
            }
            result.append(data)

        serializer = CountrySearchRatioSerializer(data=result, many=True)
        serializer.is_valid()
        
        return Response(serializer.data)


class CityViewSet(BaseLocationViewSet):
    queryset = City.objects.all()
    serializer_class = CitySerializer


class AirportViewSet(BaseLocationViewSet):
    queryset = Airport.objects.all()
    serializer_class = AirportSerializer
