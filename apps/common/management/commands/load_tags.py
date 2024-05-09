import json

from django.core.management.base import BaseCommand, CommandError

from apps.forum.models.qa_meta_models import Tag


class Command(BaseCommand):
    help = """
        Loads data from a specified JSON file into the Tag model. Sample Usage: `python manage.py load_tags tags.json`
        """

    def add_arguments(self, parser):
        parser.add_argument("json_file", type=str, help="The JSON file containing the tags data")

    def handle(self, *args, **options):
        try:
            with open(options["json_file"], "r") as file:
                tags_data = json.load(file)

            for tag in tags_data:
                Tag.objects.update_or_create(name=tag["name"], defaults={"description": tag["description"]})
            self.stdout.write(self.style.SUCCESS("Successfully loaded tags into the database"))
        except FileNotFoundError:
            raise CommandError('File "{}" does not exist'.format(options["json_file"]))
        except Exception as e:
            raise CommandError(f"An error occurred: {e}")
