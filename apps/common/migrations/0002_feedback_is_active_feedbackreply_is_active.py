# Generated by Django 4.2 on 2024-05-13 06:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("common", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="feedback",
            name="is_active",
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name="feedbackreply",
            name="is_active",
            field=models.BooleanField(default=True),
        ),
    ]
