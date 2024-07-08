import pytest

from apps.badges.models.badge_models import UserBadge
from apps.content_actions.models.vote_models import Vote
from apps.forum.models.qa_models import Answer, Post, Question
from apps.forum.tests.factories import BookmarkFactory, VoteFactory

pytestmark = pytest.mark.django_db


class TestPostModel:
    NOTABLE_BOOKMARK_POINT = 2

    def test_str(self, post: Post):
        assert str(post) == f"Post by {post.user}"

    def test_update_score(self, post: Post):
        VoteFactory.create_batch(size=3, content_object=post, vote_type=Vote.UPVOTE)
        VoteFactory.create(content_object=post, vote_type=Vote.DOWNVOTE)
        post.update_score()
        assert post.score == self.NOTABLE_BOOKMARK_POINT

    @pytest.mark.parametrize("score", [100, 25, 10])
    def test_evaluate_score_badges_question(self, question: Question, score):
        score_badge_mapping = {
            100: "Great Question",
            25: "Good Question",
            10: "Nice Question",
        }
        question.post.score = score
        question.post.evaluate_score_badges()
        assert UserBadge.objects.filter(user=question.post.user, badge__name=score_badge_mapping[score]).exists()

    @pytest.mark.parametrize("score", [100, 25, 10, 3, 1])
    def test_evaluate_score_badges_answer(self, answer: Answer, score):
        score_badge_mapping = {
            100: "Great Answer",
            25: "Good Answer",
            10: "Nice Answer",
            3: "Self-Learner",
            1: "Teacher",
        }
        answer.post.score = score
        answer.post.evaluate_score_badges()
        assert UserBadge.objects.filter(user=answer.post.user, badge__name=score_badge_mapping[score]).exists()

    @pytest.mark.parametrize("bookmark_count", [100, 25])
    def test_evaluate_bookmark_badges_question(self, question: Question, bookmark_count):
        bookmark_count_mapping = {
            100: "Stellar Question",
            25: "Favorite Question",
        }
        BookmarkFactory.create_batch(size=bookmark_count, content_object=question.post)
        question.post.evaluate_bookmark_badges()
        assert UserBadge.objects.filter(
            user=question.post.user, badge__name=bookmark_count_mapping[bookmark_count]
        ).exists()

    @pytest.mark.parametrize("bookmark_count", [100, 25])
    def test_evaluate_bookmark_badges_answer(self, answer: Answer, bookmark_count: int):
        bookmark_count_mapping = {
            100: "Stellar Answer",
            25: "Favorite Answer",
        }
        BookmarkFactory.create_batch(size=bookmark_count, content_object=answer.post)
        answer.post.evaluate_bookmark_badges()
        assert UserBadge.objects.filter(
            user=answer.post.user, badge__name=bookmark_count_mapping[bookmark_count]
        ).exists()


class TestQuestionModel:
    def test_str(self, question: Question):
        assert str(question) == question.title

    @pytest.mark.parametrize("view_count", [10_000, 2500, 1000])
    def test_check_question_view_badges(self, question: Question, view_count: int):
        view_count_mapping = {
            10_000: "Famous Question",
            2500: "Notable Question",
            1000: "Popular Question",
        }
        question.view_count = view_count
        question.check_question_view_badges()
        assert UserBadge.objects.filter(user=question.post.user, badge__name=view_count_mapping[view_count]).exists()


class TestAnswerModel:
    def test_str(self, answer: Answer):
        assert str(answer) == f"Answer to {answer.question.title}"
