import json
from datetime import datetime

import boto3
from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import transaction

from apps.entities.models import Student
from apps.entities.models.faculty_models import Department, Faculty
from apps.entities.utils import generate_password
from apps.rbac.models.role_models import Role, UserRole
from apps.users.views.user_views import User


class Command(BaseCommand):
    help = "Loads student data to the database."

    def parse_date(self, date_str):
        """
        Parse and reformat the date string to YYYY-MM-DD format.
        """
        try:
            return datetime.strptime(date_str, "%d-%m-%Y").strftime("%Y-%m-%d")
        except ValueError as e:
            self.stdout.write(self.style.ERROR(f"Date format error: {e}"))
            return None

    def handle(self, *args, **options):
        session = boto3.session.Session()
        client = session.client(
            "s3",
            endpoint_url=settings.AWS_S3_ENDPOINT_URL,
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        )

        try:
            response = client.get_object(Bucket=settings.AWS_STORAGE_BUCKET_NAME, Key="data/student_list.json")
            json_data = response["Body"].read()
            data = json.loads(json_data)
        except client.exceptions.NoSuchKey:
            self.stdout.write(self.style.ERROR("Failed to retrieve data: The specified key does not exist."))
            return
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Failed to retrieve data. Unexpected error occurred. Error: {str(e)}"))
            return
        finally:
            response["Body"].close()

        for entry in data:
            try:
                with transaction.atomic():
                    admission_date = self.parse_date(entry["admission_date"])
                    graduation_date = self.parse_date(entry["graduation_date"])

                    first_name = entry["first_name"]
                    middle_name = entry["middle_name"]
                    last_name = entry["last_name"]

                    password = generate_password(last_name)

                    user = User.objects.create_user(
                        first_name=first_name,
                        middle_name=middle_name,
                        last_name=last_name,
                        gender=entry["gender"],
                        username=entry["username"],
                        password=password,
                        is_first_time_login=True,
                    )
                    faculty = Faculty.objects.get(name=entry["faculty"])
                    department = Department.objects.get(name=entry["department"])
                    Student.objects.create(
                        user=user,
                        faculty=faculty,
                        department=department,
                        year_in_school=entry["year_in_school"],
                        admission_date=admission_date,
                        graduation_date=graduation_date,
                    )
                    role = Role.objects.get(name="Student")
                    UserRole.objects.create(user=user, role=role)
            except Exception as e:
                getattr(user, "delete", lambda: None)()
                self.stdout.write(
                    self.style.ERROR(f"Failed to create a student record for {entry['username']}. Error: {str(e)}")
                )

        self.stdout.write(self.style.SUCCESS("Successfully loaded students into the database"))
