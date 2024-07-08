from datetime import date

import pytest

from apps.badges.models.badge_models import Badge, DailyUserReputation

pytestmark = pytest.mark.django_db


class TestUserModel:
    REPUTATION_CHANGE = 50
    REPUTATION_CAP = 200
    REPUTATION_OVER_CAP = 201

    def test_str(self, user):
        assert str(user) == user.username

    def test_get_fullname(self, user):
        assert user.get_fullname == f"{user.first_name} {user.middle_name} {user.last_name}"

    def test_add_reputation(self, user):
        initial_reputation = user.reputation
        user.add_reputation(50)
        assert user.reputation == initial_reputation + 50

        # Ensure daily reputation is also updated
        daily_reputation = DailyUserReputation.objects.get(user=user, date=date.today())
        assert daily_reputation.reputation == self.REPUTATION_CHANGE

    def test_add_reputation_cap(self, user):
        user.add_reputation(190)
        user.add_reputation(20)  # Should only add 10 points to reach the cap of 200
        assert user.reputation == self.REPUTATION_OVER_CAP

        # Ensure daily reputation is capped at 200
        daily_reputation = DailyUserReputation.objects.get(user=user, date=date.today())
        assert daily_reputation.reputation == self.REPUTATION_CAP

    def test_subtract_reputation(self, user):
        user.reputation = 100
        user.save()

        user.subtract_reputation(50)
        assert user.reputation == self.REPUTATION_CHANGE

        # Ensure daily reputation is also updated
        daily_reputation = DailyUserReputation.objects.get(user=user, date=date.today())
        assert daily_reputation.reputation == 0

    def test_assign_badge(self, user):
        badge = Badge.objects.create(name="Test Badge", description="Test Badge", level=Badge.BadgeLevel.GOLD)

        user_badge = user.assign_badge("Test Badge")
        assert user_badge is not None
        assert user_badge.user == user
        assert user_badge.badge == badge

        # Test assigning the same badge again
        same_badge = user.assign_badge("Test Badge")
        assert same_badge == user_badge

        # Test assigning a non-existent badge
        non_existent_badge = user.assign_badge("Non-existent Badge")
        assert non_existent_badge is None
