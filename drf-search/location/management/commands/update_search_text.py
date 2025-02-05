from django.core.management.base import BaseCommand
from django.db import transaction
from location.models import Country, City, Airport
from tqdm import tqdm


class Command(BaseCommand):
    help = 'Updates search_text field for all location models based on their relationships'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Run without making any changes to the database',
        )
        parser.add_argument(
            '--model',
            type=str,
            choices=['all', 'country', 'city', 'airport'],
            default='all',
            help='Specify which model to update',
        )

    def handle(self, *args, **options):
        try:
            with transaction.atomic():
                if options['model'] in ['all', 'country']:
                    self.update_countries(options['dry_run'])
                
                if options['model'] in ['all', 'city']:
                    self.update_cities(options['dry_run'])
                
                if options['model'] in ['all', 'airport']:
                    self.update_airports(options['dry_run'])

                if options['dry_run']:
                    self.stdout.write(
                        self.style.SUCCESS('Dry run completed successfully')
                    )
                    # Rollback the transaction in dry run mode
                    raise Exception("Dry run mode - rolling back changes")
                
        except Exception as e:
            if not options['dry_run']:
                self.stderr.write(
                    self.style.ERROR(f'Error updating search texts: {str(e)}')
                )
                raise e

    def update_countries(self, dry_run):
        countries = Country.objects.all()
        self.stdout.write('Updating Countries...')
        
        updates = []
        for country in tqdm(countries, desc='Countries'):
            country.search_text = country.name
            updates.append(country)

        if not dry_run:
            Country.objects.bulk_update(updates, ['search_text'])
            self.stdout.write(
                self.style.SUCCESS(f'Updated {len(updates)} Countries')
            )

    def update_cities(self, dry_run):
        cities = City.objects.select_related('country').all()
        self.stdout.write('Updating Cities...')
        
        updates = []
        for city in tqdm(cities, desc='Cities'):
            city.search_text = f"{city.name},{city.country.name}"
            updates.append(city)

        if not dry_run:
            City.objects.bulk_update(updates, ['search_text'])
            self.stdout.write(
                self.style.SUCCESS(f'Updated {len(updates)} Cities')
            )

    def update_airports(self, dry_run):
        airports = Airport.objects.select_related('city', 'country').all()
        self.stdout.write('Updating Airports...')
        
        updates = []
        for airport in tqdm(airports, desc='Airports'):
            airport.search_text = (
                f"{airport.name},"
                f"{airport.city.name},"
                f"{airport.country.name}"
            )
            updates.append(airport)

        if not dry_run:
            Airport.objects.bulk_update(updates, ['search_text'])
            self.stdout.write(
                self.style.SUCCESS(f'Updated {len(updates)} Airports')
            ) 