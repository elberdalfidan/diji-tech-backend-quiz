from django.contrib import admin
from .models import Country, City, Airport


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'phone_code', 'search_count')
    search_fields = ('name', 'code')
    ordering = ('name',)


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ('name', 'country', 'search_count')
    search_fields = ('name', 'country__name')
    list_filter = ('country',)
    ordering = ('name',)


@admin.register(Airport)
class AirportAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'city', 'country', 'search_count')
    search_fields = ('name', 'code', 'city__name', 'country__name')
    list_filter = ('country', 'city')
    ordering = ('name',)
