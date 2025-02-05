from rest_framework import serializers
from .models import Country, City, Airport


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ['id', 'name', 'code', 'phone_code', 'search_count']


class CitySerializer(serializers.ModelSerializer):
    country = CountrySerializer(read_only=True)

    class Meta:
        model = City
        fields = ['id', 'name', 'country', 'search_count']


class AirportSerializer(serializers.ModelSerializer):
    country = CountrySerializer(read_only=True)
    city = CitySerializer(read_only=True)

    class Meta:
        model = Airport
        fields = ['id', 'name', 'code', 'country', 'city', 'search_count']


class CountrySearchRatioSerializer(serializers.ModelSerializer):
    search_ratio = serializers.FloatField()
    total_city_searches = serializers.IntegerField()
    total_airport_searches = serializers.IntegerField()

    class Meta:
        model = Country
        fields = ['code', 'name', 'search_ratio', 'total_city_searches', 'total_airport_searches']


class CountryCitySearchSerializer(serializers.ModelSerializer):
    most_searched_cities = CitySerializer(many=True, read_only=True)

    class Meta:
        model = Country
        fields = ['id', 'name', 'code', 'most_searched_cities']


class MostSearchedCitiesSerializer(serializers.ModelSerializer):
    most_searched_cities = serializers.SerializerMethodField()

    class Meta:
        model = Country
        fields = ['code', 'name', 'most_searched_cities']

    def get_most_searched_cities(self, obj):
        cities = obj.cities.order_by('-search_count')[:5]
        return CitySerializer(cities, many=True).data 