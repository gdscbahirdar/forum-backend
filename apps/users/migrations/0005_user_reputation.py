# Generated by Django 4.2 on 2024-05-15 07:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0004_user_gender"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="reputation",
            field=models.IntegerField(
                default=1, help_text="Reputation points earned by the user through various activities. Default is one."
            ),
        ),
    ]