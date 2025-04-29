import csv
from datetime import datetime
from django.utils import timezone
from django.core.management.base import BaseCommand
from news_recommender.models import NewsArticle

class Command(BaseCommand):
    help = 'Load news articles from CSV'

    def handle(self, *args, **kwargs):
        with open('bbc_news.csv', 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for idx, row in enumerate(reader):
                if idx >= 30000:  # ✅ Load only 30000 rows
                    break

                # Parse the pubDate
                try:
                    naive_pub_date = datetime.strptime(row['pubDate'], '%a, %d %b %Y %H:%M:%S %Z')
                    pub_date = timezone.make_aware(naive_pub_date)
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'Date parsing error for {row["guid"]}: {str(e)}'))
                    continue

                # Use get_or_create with exception handling
                try:
                    article, created = NewsArticle.objects.get_or_create(
                        guid=row['guid'],  # Ensure we're searching by guid
                        defaults={
                            'title': row['title'],
                            'pubDate': pub_date,
                            'link': row['link'],
                            'description': row['description']
                        }
                    )
                    if created:
                        self.stdout.write(self.style.SUCCESS(f'Successfully added: {row["title"]}'))
                    else:
                        self.stdout.write(f'Article with GUID {row["guid"]} already exists. Skipping.')
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'Error processing {row["guid"]}: {str(e)}'))

        self.stdout.write(self.style.SUCCESS('Data loading complete.'))
