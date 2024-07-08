import pytest
from django.core.management import call_command

from apps.forum.tests.factories import AnswerFactory, PostFactory, QuestionFactory


@pytest.fixture(autouse=True)
def badges():
    call_command("load_badges")


@pytest.fixture
def post(user):
    return PostFactory.create(user=user)


@pytest.fixture
def question(post):
    return QuestionFactory.create(post=post)


@pytest.fixture
def answer(post, question):
    return AnswerFactory.create(post=post, question=question)
