from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.password_validation import validate_password
from getpass import getpass

from apps.rbac.models.role_models import Role, UserRole

User = get_user_model()


class Command(BaseCommand):
    help = "Create a superuser with a Super Admin role"

    def handle(self, *args, **options):
        username = input("Username: ")
        first_name = input("First name: ")
        middle_name = input("Middle name: ")
        last_name = input("Last name: ")

        while True:
            password = getpass("Password: ")
            password_confirmation = getpass("Password (again): ")
            if password != password_confirmation:
                self.stderr.write("Error: Passwords do not match. Please try again.")
            else:
                try:
                    validate_password(password)
                    break
                except Exception as e:
                    self.stderr.write(f"Password validation error: {e}")

        if User.objects.filter(username=username).exists():
            raise CommandError(f"A user with username '{username}' already exists.")

        user = User.objects.create_superuser(
            username=username,
            first_name=first_name,
            middle_name=middle_name,
            last_name=last_name,
            password=password,
        )

        try:
            role = Role.objects.get(name="Super Admin")
        except Role.DoesNotExist:
            raise CommandError("Role 'Super Admin' does not exist.")

        UserRole.objects.create(user=user, role=role)

        self.stdout.write(self.style.SUCCESS("Successfully created superuser with Super Admin role."))
