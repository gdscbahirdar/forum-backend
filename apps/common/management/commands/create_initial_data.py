from django.core.management import call_command
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Load all initial data. Sample Usage: `python manage.py create_initial_data`"

    def handle(self, *args, **kwargs):
        commands = [
            "load_resource_categories",
            "load_tags",
            "load_badges",
            "load_students",
        ]

        for command in commands:
            self.stdout.write(f"Running {command}...")
            call_command(command)
