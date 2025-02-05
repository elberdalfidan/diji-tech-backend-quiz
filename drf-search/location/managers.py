from django.db import models
from django.db.models import Q
from unidecode import unidecode


class LocationQuerySet(models.QuerySet):
    def search(self, query):
        if not query:
            return self.none()
            
        # Normalize search query
        normalized_query = unidecode(query.lower())
        
        # Use basic LIKE query for SQLite
        return self.filter(
            Q(search_text__icontains=normalized_query)
        ).order_by('name')[:20]


class LocationManager(models.Manager):
    def get_queryset(self):
        return LocationQuerySet(self.model, using=self._db)
    
    def search(self, query):
        return self.get_queryset().search(query) 