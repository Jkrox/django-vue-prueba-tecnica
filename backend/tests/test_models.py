import pytest
from api.models import Category, Comment, Post
from django.contrib.auth.models import User
from django.utils import timezone


@pytest.mark.django_db
class TestCategory:
    def test_category_creation(self):
        category = Category.objects.create(
            name="Test Category", description="Test Description"
        )
        assert category.slug == "test-category"
        assert str(category) == "Test Category"


@pytest.mark.django_db
class TestPost:
    @pytest.fixture
    def user(self):
        return User.objects.create_user(username="testuser", password="12345")

    @pytest.fixture
    def category(self):
        return Category.objects.create(name="Test Category")

    def test_post_creation(self, user, category):
        post = Post.objects.create(
            title="Test Post",
            content="Test Content",
            author=user,
            category=category,
            status="draft",
        )
        assert post.slug == "test-post"
        assert str(post) == "Test Post"
        assert post.views == 0

    def test_post_scheduling(self, user, category):
        scheduled_date = timezone.now() + timezone.timedelta(days=1)
        post = Post.objects.create(
            title="Scheduled Post",
            content="Test Content",
            author=user,
            category=category,
            status="scheduled",
            scheduled_date=scheduled_date,
        )
        assert post.status == "scheduled"
        assert post.scheduled_date is not None


@pytest.mark.django_db
class TestComment:
    @pytest.fixture
    def user(self):
        return User.objects.create_user(username="testuser", password="12345")

    @pytest.fixture
    def post(self, user):
        return Post.objects.create(
            title="Test Post", content="Test Content", author=user, status="published"
        )

    def test_comment_creation(self, user, post):
        comment = Comment.objects.create(post=post, author=user, content="Test Comment")
        assert str(comment) == "Comment by testuser on Test Post"
        assert comment.is_approved is False
