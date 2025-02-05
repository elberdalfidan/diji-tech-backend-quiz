from django.test import TestCase, Client
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Country, City, Airport
from io import StringIO
from django.core.management import call_command


class LocationModelsTest(TestCase):
    def setUp(self):
        # Create test data
        self.country = Country.objects.create(
            name="Test Country",
            code="TC",
            phone_code="+99",
            search_text="Test Country"
        )
        
        self.city = City.objects.create(
            name="Test City",
            country=self.country,
            search_text="Test City,Test Country"
        )
        
        self.airport = Airport.objects.create(
            name="Test Airport",
            code="TST",
            country=self.country,
            city=self.city,
            search_text="Test Airport,Test City,Test Country"
        )

    def test_model_creation(self):
        """Test model instances are created correctly"""
        self.assertEqual(self.country.name, "Test Country")
        self.assertEqual(self.city.name, "Test City")
        self.assertEqual(self.airport.code, "TST")

    def test_model_relationships(self):
        """Test model relationships are working"""
        self.assertEqual(self.city.country, self.country)
        self.assertEqual(self.airport.city, self.city)
        self.assertEqual(self.airport.country, self.country)

    def test_search_count_increment(self):
        """Test search count increment functionality"""
        initial_count = self.country.search_count
        self.country.increment_search_count()
        self.assertEqual(self.country.search_count, initial_count + 1)


class LocationAPITest(APITestCase):
    def setUp(self):
        self.client = Client()
        
        # Create test data
        self.country = Country.objects.create(
            name="Test Country",
            code="TC",
            phone_code="+99",
            search_text="Test Country"
        )
        
        self.city = City.objects.create(
            name="Test City",
            country=self.country,
            search_text="Test City,Test Country"
        )
        
        self.airport = Airport.objects.create(
            name="Test Airport",
            code="TST",
            country=self.country,
            city=self.city,
            search_text="Test Airport,Test City,Test Country"
        )

    def test_search_endpoints(self):
        """Test search functionality for all models"""
        # Test country search
        response = self.client.get(reverse('countries-search'), {'q': 'Test'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

        # Test city search
        response = self.client.get(reverse('cities-search'), {'q': 'Test'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

        # Test airport search
        response = self.client.get(reverse('airports-search'), {'q': 'Test'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_select_endpoints(self):
        """Test select functionality for all models"""
        # Test country selection
        response = self.client.post(reverse('countries-select', args=[self.country.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('selected_countries' in response.cookies)

        # Test city selection
        response = self.client.post(reverse('cities-select', args=[self.city.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('selected_cities' in response.cookies)

        # Test airport selection
        response = self.client.post(reverse('airports-select', args=[self.airport.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('selected_airports' in response.cookies)

    def test_deselect_endpoints(self):
        """Test deselect functionality for all models"""
        # First select, then deselect for country
        self.client.post(reverse('countries-select', args=[self.country.id]))
        response = self.client.post(reverse('countries-deselect'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.cookies['selected_countries'].value, '')

    def test_most_searched_cities(self):
        """Test most searched cities endpoint"""
        response = self.client.get(
            reverse('countries-most-searched-cities'),
            {'country_code': self.country.code}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('most_searched_cities' in response.data[0])

    def test_search_ratio(self):
        """Test search ratio endpoint"""
        # Increment some search counts
        self.city.increment_search_count()
        self.airport.increment_search_count()
        
        response = self.client.get(
            reverse('countries-search-ratio'),
            {'country_code': self.country.code}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('search_ratio' in response.data[0])

    def test_search_with_accents(self):
        """Test search functionality with accented characters"""
        special_city = City.objects.create(
            name="İstanbul",
            country=self.country,
            search_text="İstanbul,Test Country"
        )
        
        response = self.client.get(reverse('cities-search'), {'q': 'istanbul'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_multiple_country_codes(self):
        """Test endpoints with multiple country codes"""
        country2 = Country.objects.create(
            name="Second Country",
            code="SC",
            phone_code="+88",
            search_text="Second Country"
        )
        
        response = self.client.get(
            reverse('countries-search-ratio'),
            {'country_code': f'{self.country.code},{country2.code}'}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)


class LocationMiddlewareTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.country = Country.objects.create(
            name="Test Country",
            code="TC",
            phone_code="+99",
            search_text="Test Country"
        )

    def test_search_count_middleware(self):
        """Test if search count increases when location is selected"""
        initial_count = self.country.search_count
        
        # Select country and make a request
        self.client.post(reverse('countries-select', args=[self.country.id]))
        self.client.get(reverse('countries-list'))
        
        # Refresh from database
        self.country.refresh_from_db()
        self.assertEqual(self.country.search_count, initial_count + 1)

    def test_search_count_on_error(self):
        """Test that search count doesn't increase on error responses"""
        initial_count = self.country.search_count
        
        # Make request to non-existent endpoint
        self.client.get('/api/non-existent/')
        
        self.country.refresh_from_db()
        self.assertEqual(self.country.search_count, initial_count)


class UpdateSearchTextCommandTest(TestCase):
    def setUp(self):
        # Create test data
        self.country = Country.objects.create(
            name="Test Country",
            code="TC",
            phone_code="+99"
        )
        self.city = City.objects.create(
            name="Test City",
            country=self.country
        )
        self.airport = Airport.objects.create(
            name="Test Airport",
            code="TST",
            city=self.city,
            country=self.country
        )

    def test_command_output(self):
        out = StringIO()
        call_command('update_search_text', stdout=out)
        
        # Verify the objects were updated
        self.country.refresh_from_db()
        self.city.refresh_from_db()
        self.airport.refresh_from_db()
        
        self.assertEqual(self.country.search_text, "Test Country")
        self.assertEqual(self.city.search_text, "Test City,Test Country")
        self.assertEqual(
            self.airport.search_text,
            "Test Airport,Test City,Test Country"
        )

    def test_dry_run(self):
        out = StringIO()
        call_command('update_search_text', '--dry-run', stdout=out)
        
        # Verify no changes were made
        self.country.refresh_from_db()
        self.city.refresh_from_db()
        self.airport.refresh_from_db()
        
        self.assertEqual(self.country.search_text, "")
        self.assertEqual(self.city.search_text, "")
        self.assertEqual(self.airport.search_text, "")