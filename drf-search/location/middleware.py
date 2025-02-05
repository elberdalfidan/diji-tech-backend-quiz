from django.http import HttpResponse
from .models import Country, City, Airport, APILog
import time
import logging

logger = logging.getLogger('api')

class LocationSearchCountMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        
        # Only process if response is successful
        if not isinstance(response, HttpResponse) or response.status_code != 200:
            return response

        self._increment_search_counts(request)
        return response

    def _increment_search_counts(self, request):
        model_cookie_mapping = {
            'selected_country': Country,
            'selected_city': City,
            'selected_airport': Airport,
        }

        for cookie_name, model in model_cookie_mapping.items():
            location_id = request.COOKIES.get(cookie_name)
            if location_id:
                try:
                    instance = model.objects.get(id=location_id)
                    instance.increment_search_count()
                    
                    # Increment parent models' search count
                    if hasattr(instance, 'country'):
                        instance.country.increment_search_count()
                    if hasattr(instance, 'city'):
                        instance.city.increment_search_count()
                except model.DoesNotExist:
                    pass

class APILoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start_time = time.time()
        
        response = self.get_response(request)
        
        # DB Log
        if request.path.startswith('/api/'):
            duration = time.time() - start_time
            APILog.objects.create(
                path=request.path,
                method=request.method,
                status_code=response.status_code,
                response_time=duration * 1000,  # convert to ms
                user_agent=request.META.get('HTTP_USER_AGENT'),
                ip_address=self.get_client_ip(request),
                request_data=self.get_request_data(request),
                response_data=self.get_response_data(response)
            )
            
            # File Log
            logger.info(
                f"[{request.method}] {request.path} "
                f"- Status: {response.status_code} "
                f"- Duration: {duration:.2f}s "
                f"- IP: {self.get_client_ip(request)}"
            )
        
        return response

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0]
        return request.META.get('REMOTE_ADDR')

    def get_request_data(self, request):
        if request.method in ['POST', 'PUT', 'PATCH']:
            return request.POST.dict()
        return request.GET.dict()

    def get_response_data(self, response):
        try:
            return response.data
        except AttributeError:
            return None 