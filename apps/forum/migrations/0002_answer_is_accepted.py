# Generated by Django 4.2 on 2024-04-09 15:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("forum", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="answer",
            name="is_accepted",
            field=models.BooleanField(default=False),
        ),
    ]