from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError

from apps.rbac.models.role_models import Role, UserRole

User = get_user_model()


class Command(BaseCommand):
    help = "Create a superuser with a Super Admin role"

    def add_arguments(self, parser):
        parser.add_argument("--username", type=str, help="The username of the new superuser")
        parser.add_argument("--first_name", type=str, help="The firstname of the new superuser")
        parser.add_argument("--middle_name", type=str, help="The middle name of the new superuser")
        parser.add_argument("--last_name", type=str, help="The lastname of the new superuser")
        parser.add_argument("--password", type=str, help="The password of the new superuser")

    def handle(self, *args, **options):
        username = options["username"]
        first_name = options["first_name"]
        middle_name = options["middle_name"]
        last_name = options["last_name"]
        password = options["password"]

        if User.objects.filter(username=username).exists():
            raise CommandError(f"A user with username '{username}' already exists.")

        user = User.objects.create_superuser(
            username=username, first_name=first_name, middle_name=middle_name, last_name=last_name, password=password
        )
        role = Role.objects.get(name="Super Admin")
        UserRole.objects.create(user=user, role=role)

        self.stdout.write(self.style.SUCCESS("Successfully created superuser with Super Admin role."))
