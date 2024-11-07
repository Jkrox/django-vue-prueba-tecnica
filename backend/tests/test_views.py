import pytest
from api.models import Category, Comment, Post
from django.contrib.auth.models import User
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APIClient


@pytest.mark.django_db
class TestPostViews:
    @pytest.fixture
    def api_client(self):
        return APIClient()

    @pytest.fixture
    def user(self):
        return User.objects.create_user(
            username="testuser", password="testpass123", email="test@example.com"
        )

    @pytest.fixture
    def category(self):
        return Category.objects.create(name="Test Category")

    def test_post_list_pagination(self, api_client, user, category):
        # Create 15 posts
        for i in range(15):
            Post.objects.create(
                title=f"Test Post {i}",
                content=f"Content {i}",
                author=user,
                category=category,
                status="published",
                published_date=timezone.now(),
            )

        response = api_client.get("/api/posts/")
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["results"]) == 10  # Default pagination
        assert response.data["count"] == 15

    def test_post_filtering(self, api_client, user, category):
        Post.objects.create(
            title="Django Post",
            content="Django content",
            author=user,
            category=category,
            status="published",
            published_date=timezone.now(),
        )
        Post.objects.create(
            title="Vue Post",
            content="Vue content",
            author=user,
            category=category,
            status="draft",
        )

        # Test status filter
        response = api_client.get("/api/posts/", {"status": "published"})
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["results"]) == 1
        assert response.data["results"][0]["title"] == "Django Post"

        # Test search
        response = api_client.get("/api/posts/", {"search": "Django"})
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["results"]) == 1
        assert "Django" in response.data["results"][0]["title"]


@pytest.mark.django_db
class TestCommentViews:
    @pytest.fixture
    def api_client(self):
        return APIClient()

    @pytest.fixture
    def user(self):
        return User.objects.create_user(username="testuser", password="testpass123")

    @pytest.fixture
    def post(self, user):
        return Post.objects.create(
            title="Test Post",
            content="Test content",
            author=user,
            status="published",
            published_date=timezone.now(),
        )

    def test_create_comment(self, api_client, user, post):
        api_client.force_authenticate(user=user)
        data = {"post": post.id, "content": "Test comment", "author_id": user.id}
        response = api_client.post("/api/comments/", data)
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["content"] == "Test comment"

    def test_comment_list_filtering(self, api_client, user, post):
        Comment.objects.create(
            post=post, author=user, content="First comment", is_approved=True
        )
        Comment.objects.create(
            post=post, author=user, content="Second comment", is_approved=False
        )

        response = api_client.get("/api/comments/", {"is_approved": "true"})
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["results"]) == 1
        assert response.data["results"][0]["content"] == "First comment"
