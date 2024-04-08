# Generated by Django 4.2.11 on 2024-04-08 07:31

from django.db import migrations


def populate_faculty_and_department(apps, schema_editor):
    Faculty = apps.get_model("entities", "Faculty")
    Department = apps.get_model("entities", "Department")

    # Creating Faculty instances
    faculty_computing = Faculty.objects.create(
        name="FACULTY OF COMPUTING", description="Faculty dedicated to computing disciplines."
    )

    # Creating Department instances and linking them to the Faculty of Computing
    departments = [
        ("COMPUTER SCIENCE", "Computer Science"),
        ("INFORMATION TECHNOLOGY", "Information Technology"),
        ("SOFTWARE ENGINEERING", "Software Engineering"),
        ("INFORMATION SYSTEMS", "Information Systems"),
        ("CYBER SECURITY", "Cyber Security"),
    ]

    for name, description in departments:
        Department.objects.create(name=name, description=f"Department of {description}", faculty=faculty_computing)


class Migration(migrations.Migration):

    dependencies = [
        ("entities", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(populate_faculty_and_department),
    ]
