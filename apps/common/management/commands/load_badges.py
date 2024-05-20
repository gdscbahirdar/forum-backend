from django.core.management.base import BaseCommand

from apps.badges.models.badge_models import Badge


class Command(BaseCommand):
    help = "Creates predefined badges in the database."

    def handle(self, *args, **options):
        badges = [
            {
                "name": "Favorite Question",
                "description": "Question saved by 25 users",
                "level": Badge.BadgeLevel.SILVER,
            },
            {
                "name": "Stellar Question",
                "description": "Question saved by 100 users",
                "level": Badge.BadgeLevel.GOLD,
            },
            {
                "name": "Nice Question",
                "description": "Question score of 10 or more",
                "level": Badge.BadgeLevel.BRONZE,
            },
            {
                "name": "Good Question",
                "description": "Question score of 25 or more",
                "level": Badge.BadgeLevel.SILVER,
            },
            {
                "name": "Great Question",
                "description": "Question score of 100 or more",
                "level": Badge.BadgeLevel.GOLD,
            },
            {
                "name": "Popular Question",
                "description": "Question with 500 views",
                "level": Badge.BadgeLevel.BRONZE,
            },
            {
                "name": "Notable Question",
                "description": "Question with 750 views",
                "level": Badge.BadgeLevel.SILVER,
            },
            {
                "name": "Famous Question",
                "description": "Question with 1000 views",
                "level": Badge.BadgeLevel.GOLD,
            },
            {
                "name": "Favorite Answer",
                "description": "Answer saved by 25 users",
                "level": Badge.BadgeLevel.SILVER,
            },
            {
                "name": "Stellar Answer",
                "description": "Answer saved by 100 users",
                "level": Badge.BadgeLevel.GOLD,
            },
            {
                "name": "Guru",
                "description": "Accepted answer and score of 40 or more",
                "level": Badge.BadgeLevel.SILVER,
            },
            {
                "name": "Nice Answer",
                "description": "Answer score of 10 or more",
                "level": Badge.BadgeLevel.BRONZE,
            },
            {
                "name": "Good Answer",
                "description": "Answer score of 25 or more",
                "level": Badge.BadgeLevel.SILVER,
            },
            {
                "name": "Great Answer",
                "description": "Answer score of 100 or more",
                "level": Badge.BadgeLevel.GOLD,
            },
            {
                "name": "Self-Learner",
                "description": "Answer your own question with score of 3 or more",
                "level": Badge.BadgeLevel.BRONZE,
            },
            {
                "name": "Teacher",
                "description": "Answer a question with score of 1 or more",
                "level": Badge.BadgeLevel.BRONZE,
            },
        ]

        for badge_data in badges:
            Badge.objects.update_or_create(name=badge_data["name"], defaults=badge_data)

        self.stdout.write(self.style.SUCCESS("All badges have been created/updated successfully!"))
