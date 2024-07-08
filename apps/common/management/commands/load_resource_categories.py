import json
import os

from django.conf import settings
from django.core.management.base import BaseCommand
from django.core.management.base import CommandError

from apps.resources.models.resource_models import ResourceCategory


class Command(BaseCommand):
    help = """
        Loads data from a specified JSON file into the category model. Sample Usage: `python manage.py`
        """

    def handle(self, *args, **options):
        try:
            file_path = os.path.join(
                settings.BASE_DIR, "../apps", "common", "initial_data", "resource_categories.json"
            )
            with open(file_path, "r") as file:
                category_data = json.load(file)

            for category in category_data:
                ResourceCategory.objects.update_or_create(
                    name=category["name"], defaults={"description": category["description"]}
                )
            self.stdout.write(self.style.SUCCESS("Successfully loaded resource categories into the database"))
        except FileNotFoundError:
            raise CommandError('File "{}" does not exist'.format(file_path))
        except Exception as e:
            raise CommandError(f"An error occurred: {e}")
