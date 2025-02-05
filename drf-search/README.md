# Location Management System API

A Django REST Framework-based API for managing locations (countries, cities, and airports) with advanced search capabilities and usage analytics.

## Features

- Location management (Countries, Cities, Airports)
- Advanced search functionality (case-insensitive and accent-insensitive)
- Search statistics tracking
- Cookie-based location selection
- Comprehensive REST API endpoints
- Swagger/OpenAPI documentation
- API request logging (both file and database)

## Tech Stack

- Python 3.8+
- Django 4.2+
- Django REST Framework
- PostgreSQL/SQLite
- Swagger/OpenAPI Documentation

## Installation

1. Clone the repository

2. Create and activate virtual environment

```bash
python -m venv venv
source venv/bin/activate # On Windows: venv\Scripts\activate
```

3. Install dependencies

```bash
pip install -r requirements.txt
```

4. Create `.env` file and set environment variables

```bash
cp .env.example .env
```

5. Apply migrations

```bash
python manage.py migrate
```

6. Run development server

```bash
python manage.py runserver
```

## API Documentation

The API documentation is available through Swagger UI and ReDoc:
- Swagger UI: `/swagger/`
- ReDoc: `/redoc/`

### Main Endpoints

#### Location Models (Countries, Cities, Airports)
- `GET /api/{model}/` - List all items
- `GET /api/{model}/{id}/` - Retrieve specific item
- `POST /api/{model}/{id}/select/` - Select a location
- `POST /api/{model}/deselect/` - Deselect current location
- `GET /api/{model}/search/?q={query}` - Search locations

#### Country-specific Endpoints
- `GET /api/countries/most_searched_cities/?country_code=TR,UK` - Get top 5 most searched cities
- `GET /api/countries/search_ratio/?country_code=TR,UK` - Get city/airport search ratio statistics

### Example Requests

1. Search for locations

```bash
curl -X GET "http://localhost:8000/api/cities/search/?q=ankara"
```

2. Select a location

```bash
curl -X POST "http://localhost:8000/api/cities/1/select/"
```

3. Deselect current location

```bash
curl -X POST "http://localhost:8000/api/cities/deselect/"
```

4. Get most searched cities

```bash
curl "http://localhost:8000/api/countries/most_searched_cities/?country_code=TR,UK"
```

## Data Models

### Country

- `name`: CharField
- `search_text`: TextField
- `search_count`: IntegerField
- `code`: CharField
- `phone`: CharField

### City

- `name`: CharField
- `search_text`: TextField
- `search_count`: IntegerField
- `country`: ForeignKey to Country model

### Airport

- `name`: CharField
- `search_text`: TextField
- `search_count`: IntegerField
- `code`: CharField
- `country`: ForeignKey to Country model
- `city`: ForeignKey to City model

## Features in Detail

### Search Functionality

- Case-insensitive and accent-insensitive search
- Search across related models
- Maximum 20 results per query
- Search count tracking

### Location Selection

- Cookie-based location selection
- One location selection per user
- 24-hour cookie expiration
- Automatic search count increment
  

### Statistics

- Track search counts for all models
- Calculate city/airport search ratios
- Track most searched cities per country

### Logging

- File-based logging for API requests
- Database logging for deatiled aalytics
- Log rotation (5MB per file, 5 backup files)
- IP address and user agent tracking

## Development

### Running Tests

```bash
python manage.py test location 
```

For more details, run:

```bash
python manage.py test location --verbosity=2
```


### Acknowledgements

- Django REST Framework
- Swagger/OpenAPI Documentation
- PostgreSQL
- SQLite
- Python 3.8+











