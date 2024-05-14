from django.core.management.base import BaseCommand

from apps.badges.models.badge_models import Badge


class Command(BaseCommand):
    help = "Creates predefined badges in the database."

    def handle(self, *args, **options):
        badges = [
            {
                "name": "Curious",
                "description": "Ask a well-received question on 5 separate days, and maintain a positive question record",  # noqa: E501
                "points": 0,
                "level": Badge.BadgeLevel.BRONZE,
            },
            {
                "name": "Inquisitive",
                "description": "Ask a well-received question on 30 separate days, and maintain a positive question record",  # noqa: E501
                "points": 0,
                "level": Badge.BadgeLevel.SILVER,
            },
            {
                "name": "Socratic",
                "description": "Ask a well-received question on 100 separate days, and maintain a positive question record",  # noqa: E501
                "points": 0,
                "level": Badge.BadgeLevel.GOLD,
            },
            {
                "name": "Favorite Question",
                "description": "Question saved by 25 users",
                "points": 0,
                "level": Badge.BadgeLevel.SILVER,
            },
            {
                "name": "Stellar Question",
                "description": "Question saved by 100 users",
                "points": 0,
                "level": Badge.BadgeLevel.GOLD,
            },
            {
                "name": "Nice Question",
                "description": "Question score of 10 or more",
                "points": 0,
                "level": Badge.BadgeLevel.BRONZE,
            },
            {
                "name": "Good Question",
                "description": "Question score of 25 or more",
                "points": 0,
                "level": Badge.BadgeLevel.SILVER,
            },
            {
                "name": "Great Question",
                "description": "Question score of 100 or more",
                "points": 0,
                "level": Badge.BadgeLevel.GOLD,
            },
            {
                "name": "Popular Question",
                "description": "Question with 1,000 views",
                "points": 0,
                "level": Badge.BadgeLevel.BRONZE,
            },
            {
                "name": "Notable Question",
                "description": "Question with 2,500 views",
                "points": 0,
                "level": Badge.BadgeLevel.SILVER,
            },
            {
                "name": "Famous Question",
                "description": "Question with 10,000 views",
                "points": 0,
                "level": Badge.BadgeLevel.GOLD,
            },
            {
                "name": "Scholar",
                "description": "Ask a question and accept an answer",
                "points": 0,
                "level": Badge.BadgeLevel.BRONZE,
            },
            {
                "name": "Student",
                "description": "First question with score of 1 or more",
                "points": 0,
                "level": Badge.BadgeLevel.BRONZE,
            },
            {
                "name": "Favorite Answer",
                "description": "Answer saved by 25 users",
                "points": 0,
                "level": Badge.BadgeLevel.SILVER,
            },
            {
                "name": "Stellar Answer",
                "description": "Answer saved by 100 users",
                "points": 0,
                "level": Badge.BadgeLevel.GOLD,
            },
            {
                "name": "Guru",
                "description": "Accepted answer and score of 40 or more",
                "points": 0,
                "level": Badge.BadgeLevel.SILVER,
            },
            {
                "name": "Nice Answer",
                "description": "Answer score of 10 or more",
                "points": 0,
                "level": Badge.BadgeLevel.BRONZE,
            },
            {
                "name": "Good Answer",
                "description": "Answer score of 25 or more",
                "points": 0,
                "level": Badge.BadgeLevel.SILVER,
            },
            {
                "name": "Great Answer",
                "description": "Answer score of 100 or more",
                "points": 0,
                "level": Badge.BadgeLevel.GOLD,
            },
            {
                "name": "Self-Learner",
                "description": "Answer your own question with score of 3 or more",
                "points": 0,
                "level": Badge.BadgeLevel.BRONZE,
            },
            {
                "name": "Teacher",
                "description": "Answer a question with score of 1 or more",
                "points": 0,
                "level": Badge.BadgeLevel.BRONZE,
            },
        ]

        for badge_data in badges:
            Badge.objects.update_or_create(name=badge_data["name"], defaults=badge_data)

        self.stdout.write(self.style.SUCCESS("All badges have been created/updated successfully!"))
