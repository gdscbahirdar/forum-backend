# Generated by Django 4.2 on 2024-05-30 22:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("common", "0002_feedback_is_active_feedbackreply_is_active"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="feedbackreply",
            name="feedback",
        ),
        migrations.RemoveField(
            model_name="feedbackreply",
            name="user",
        ),
        migrations.DeleteModel(
            name="Feedback",
        ),
        migrations.DeleteModel(
            name="FeedbackReply",
        ),
    ]
