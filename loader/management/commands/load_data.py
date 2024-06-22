# loader/management/commands/load_data.py

import csv
from django.core.management.base import BaseCommand
from ott_recommend.models import Content
from datetime import datetime

class Command(BaseCommand):
    help = 'Load data from netflix_titles.csv into Content model'

    def handle(self, *args, **kwargs):
        with open('/Users/jiho/Desktop/netflix_titles.csv', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                content, created = Content.objects.get_or_create(
                    title=row['title'],
                    genre=row['listed_in'],
                    release_date=datetime.strptime(row['release_year'], '%Y').date(),
                    rating=row.get('rating', None),
                    description=row.get('description', ''),
                    director=row.get('director', ''),
                    cast=row.get('cast', ''),
                    country=row.get('country', ''),
                    duration=row.get('duration', '')
                )
                if created:
                    self.stdout.write(self.style.SUCCESS(f'Successfully created content: {row["title"]}'))
                else:
                    self.stdout.write(f'Content already exists: {row["title"]}')
