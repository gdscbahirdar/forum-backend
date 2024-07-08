import json
import os

from django.conf import settings
from django.core.management.base import BaseCommand
from django.core.management.base import CommandError

from apps.forum.models.qa_meta_models import Tag


class Command(BaseCommand):
    help = """
        Loads data from a specified JSON file into the Tag model. Sample Usage: `python manage.py load_tags`
        """

    def handle(self, *args, **options):
        try:
            file_path = os.path.join(settings.BASE_DIR, "../apps", "common", "initial_data", "tags.json")
            with open(file_path, "r") as file:
                tags_data = json.load(file)

            for tag in tags_data:
                Tag.objects.update_or_create(name=tag["name"], defaults={"description": tag["description"]})
            self.stdout.write(self.style.SUCCESS("Successfully loaded tags into the database"))
        except FileNotFoundError:
            raise CommandError('File "{}" does not exist'.format(file_path))
        except Exception as e:
            raise CommandError(f"An error occurred: {e}")
