from django.db import migrations
from django.db.migrations import RunPython


def load_initial_data(apps, schema_editor):
    Country = apps.get_model('location', 'Country')
    City = apps.get_model('location', 'City')
    Airport = apps.get_model('location', 'Airport')

    # Countries
    tr = Country.objects.create(
        name="Turkey",
        code="TR",
        phone_code="+90",
        search_text="Turkey"
    )
    uk = Country.objects.create(
        name="United Kingdom",
        code="UK",
        phone_code="+44",
        search_text="United Kingdom"
    )
    us = Country.objects.create(
        name="United States",
        code="US",
        phone_code="+1",
        search_text="United States"
    )

    # Turkish Cities and Airports
    tr_cities_airports = {
        "Istanbul": [
            ("Istanbul Airport", "IST"),
            ("Sabiha Gökçen Airport", "SAW"),
        ],
        "Ankara": [
            ("Esenboğa Airport", "ESB"),
        ],
        "İzmir": [
            ("Adnan Menderes Airport", "ADB"),
        ],
        "Antalya": [
            ("Antalya Airport", "AYT"),
            ("Gazipaşa Airport", "GZP"),
        ],
        "Muğla": [
            ("Dalaman Airport", "DLM"),
            ("Milas-Bodrum Airport", "BJV"),
        ],
        "Bursa": [
            ("Yenişehir Airport", "YEI"),
        ],
        "Adana": [
            ("Şakirpaşa Airport", "ADA"),
        ],
        "Trabzon": [
            ("Trabzon Airport", "TZX"),
        ],
        "Gaziantep": [
            ("Gaziantep Airport", "GZT"),
        ],
        "Kayseri": [
            ("Erkilet Airport", "ASR"),
        ],
        "Diyarbakır": [
            ("Diyarbakır Airport", "DIY"),
        ],
        "Van": [
            ("Ferit Melen Airport", "VAN"),
        ],
        "Erzurum": [
            ("Erzurum Airport", "ERZ"),
        ],
        "Samsun": [
            ("Çarşamba Airport", "SZF"),
        ],
        "Konya": [
            ("Konya Airport", "KYA"),
        ],
        "Hatay": [
            ("Hatay Airport", "HTY"),
        ],
        "Malatya": [
            ("Erhaç Airport", "MLX"),
        ],
        "Denizli": [
            ("Çardak Airport", "DNZ"),
        ],
        "Sivas": [
            ("Nuri Demirağ Airport", "VAS"),
        ],
        "Şanlıurfa": [
            ("GAP Airport", "GNY"),
        ],
    }

    # UK Cities and Airports
    uk_cities_airports = {
        "London": [
            ("Heathrow Airport", "LHR"),
            ("Gatwick Airport", "LGW"),
            ("Stansted Airport", "STN"),
            ("Luton Airport", "LTN"),
            ("London City Airport", "LCY"),
        ],
        "Manchester": [
            ("Manchester Airport", "MAN"),
        ],
        "Birmingham": [
            ("Birmingham Airport", "BHX"),
        ],
        "Glasgow": [
            ("Glasgow Airport", "GLA"),
            ("Glasgow Prestwick Airport", "PIK"),
        ],
        "Edinburgh": [
            ("Edinburgh Airport", "EDI"),
        ],
        "Bristol": [
            ("Bristol Airport", "BRS"),
        ],
        "Liverpool": [
            ("Liverpool John Lennon Airport", "LPL"),
        ],
        "Newcastle": [
            ("Newcastle Airport", "NCL"),
        ],
        "Leeds": [
            ("Leeds Bradford Airport", "LBA"),
        ],
        "Aberdeen": [
            ("Aberdeen Airport", "ABZ"),
        ],
        "Belfast": [
            ("Belfast International Airport", "BFS"),
            ("George Best Belfast City Airport", "BHD"),
        ],
        "Cardiff": [
            ("Cardiff Airport", "CWL"),
        ],
        "Nottingham": [
            ("East Midlands Airport", "EMA"),
        ],
        "Southampton": [
            ("Southampton Airport", "SOU"),
        ],
        "Exeter": [
            ("Exeter Airport", "EXT"),
        ],
    }

    # US Cities and Airports
    us_cities_airports = {
        "New York": [
            ("John F. Kennedy International Airport", "JFK"),
            ("LaGuardia Airport", "LGA"),
            ("Newark Liberty International Airport", "EWR"),
        ],
        "Los Angeles": [
            ("Los Angeles International Airport", "LAX"),
            ("Hollywood Burbank Airport", "BUR"),
        ],
        "Chicago": [
            ("O'Hare International Airport", "ORD"),
            ("Chicago Midway International Airport", "MDW"),
        ],
        "Miami": [
            ("Miami International Airport", "MIA"),
            ("Fort Lauderdale–Hollywood International Airport", "FLL"),
        ],
        "Dallas": [
            ("Dallas/Fort Worth International Airport", "DFW"),
            ("Dallas Love Field", "DAL"),
        ],
        "Houston": [
            ("George Bush Intercontinental Airport", "IAH"),
            ("William P. Hobby Airport", "HOU"),
        ],
        "Washington": [
            ("Ronald Reagan Washington National Airport", "DCA"),
            ("Washington Dulles International Airport", "IAD"),
        ],
        "San Francisco": [
            ("San Francisco International Airport", "SFO"),
            ("Oakland International Airport", "OAK"),
        ],
        "Las Vegas": [
            ("Harry Reid International Airport", "LAS"),
        ],
        "Boston": [
            ("Logan International Airport", "BOS"),
        ],
        "Atlanta": [
            ("Hartsfield–Jackson Atlanta International Airport", "ATL"),
        ],
        "Seattle": [
            ("Seattle–Tacoma International Airport", "SEA"),
        ],
        "Denver": [
            ("Denver International Airport", "DEN"),
        ],
        "Phoenix": [
            ("Phoenix Sky Harbor International Airport", "PHX"),
        ],
        "Orlando": [
            ("Orlando International Airport", "MCO"),
        ],
    }

    # Helper function to create cities and airports
    def create_cities_and_airports(country, cities_airports_data):
        cities = {}
        for city_name, airports in cities_airports_data.items():
            # Create city
            city = City.objects.create(
                name=city_name,
                country=country,
                search_text=f"{city_name},{country.name}"
            )
            cities[city_name] = city

            # Create airports for the city
            for airport_name, code in airports:
                Airport.objects.create(
                    name=airport_name,
                    code=code,
                    city=city,
                    country=country,
                    search_text=f"{airport_name},{city_name},{country.name}"
                )
        return cities

    # Create all cities and airports
    create_cities_and_airports(tr, tr_cities_airports)
    create_cities_and_airports(uk, uk_cities_airports)
    create_cities_and_airports(us, us_cities_airports)


def reverse_initial_data(apps, schema_editor):
    Country = apps.get_model('location', 'Country')
    Country.objects.all().delete()


class Migration(migrations.Migration):
    dependencies = [
        ('location', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(load_initial_data, reverse_initial_data),
    ] 