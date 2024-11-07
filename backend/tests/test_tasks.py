from datetime import timedelta

import pytest
from api.models import Post
from api.tasks import clean_old_draft_posts, schedule_post_publication
from django.contrib.auth.models import User
from django.utils import timezone


@pytest.mark.django_db
class TestPostTasks:
    @pytest.fixture
    def user(self):
        return User.objects.create_user(username="testuser", password="12345")

    def test_schedule_post_publication(self, user):
        # Create a scheduled post
        post = Post.objects.create(
            title="Scheduled Post",
            content="Test Content",
            author=user,
            status="scheduled",
            scheduled_date=timezone.now() - timedelta(minutes=5),
        )

        # Run the task
        result = schedule_post_publication(post.id)

        # Refresh the post from db
        post.refresh_from_db()

        assert post.status == "published"
        assert post.published_date is not None
        assert "Successfully published" in result

    def test_clean_old_draft_posts(self, user):
        # Create some old draft posts
        old_post = Post.objects.create(
            title="Old Draft",
            content="Test Content",
            author=user,
            status="draft",
            created_at=timezone.now() - timedelta(days=31),
        )

        # Create a recent draft post
        recent_post = Post.objects.create(
            title="Recent Draft",
            content="Test Content",
            author=user,
            status="draft",
            created_at=timezone.now(),
        )

        # Run the cleaning task
        result = clean_old_draft_posts()

        # Verify that only old drafts were deleted
        assert Post.objects.filter(id=old_post.id).count() == 0
        assert Post.objects.filter(id=recent_post.id).count() == 1
        assert "Deleted" in result

    def test_schedule_post_publication_invalid_id(self):
        result = schedule_post_publication(999999)
        assert "not found" in result

    def test_schedule_post_publication_already_published(self, user):
        post = Post.objects.create(
            title="Already Published",
            content="Test Content",
            author=user,
            status="published",
            published_date=timezone.now(),
        )

        result = schedule_post_publication(post.id)
        post.refresh_from_db()

        # Verify that the post status didn't change
        assert post.status == "published"
        assert isinstance(result, str)
