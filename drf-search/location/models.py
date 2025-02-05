from django.db import models
from location.managers import LocationManager

class BaseLocationModel(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False)
    search_text = models.TextField(null=False, blank=False)
    search_count = models.IntegerField(default=0, null=False)
    
    objects = LocationManager()

    class Meta:
        abstract = True

    def increment_search_count(self):
        self.search_count += 1
        self.save()

class Country(BaseLocationModel):
    code = models.CharField(max_length=3, unique=True)
    phone_code = models.CharField(max_length=5)

    class Meta:
        verbose_name_plural = "Countries"

    def __str__(self):
        return f"{self.name} ({self.code})"

class City(BaseLocationModel):
    country = models.ForeignKey(
        Country,
        on_delete=models.CASCADE,
        related_name='cities'
    )

    class Meta:
        verbose_name_plural = "Cities"

    def __str__(self):
        return f"{self.name}, {self.country.name}"

class Airport(BaseLocationModel):
    code = models.CharField(max_length=3, unique=True)
    country = models.ForeignKey(
        Country,
        on_delete=models.CASCADE,
        related_name='airports'
    )
    city = models.ForeignKey(
        City,
        on_delete=models.CASCADE,
        related_name='airports'
    )

    def __str__(self):
        return f"{self.name} ({self.code})"

class APILog(models.Model):
    path = models.CharField(max_length=255)
    method = models.CharField(max_length=10)
    status_code = models.IntegerField()
    response_time = models.FloatField()  # ms type
    user_agent = models.TextField(null=True)
    ip_address = models.GenericIPAddressField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    request_data = models.JSONField(null=True)
    response_data = models.JSONField(null=True)

    class Meta:
        ordering = ['-created_at']
