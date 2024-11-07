from datetime import timedelta

import pytest
from django.contrib.auth.models import User
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APIClient

from .models import Category, Post
from .tasks import schedule_post_publication


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user():
    return User.objects.create_user(username="testuser", password="testpass123")


@pytest.fixture
def category():
    return Category.objects.create(name="Test Category", slug="test-category")


@pytest.fixture
def post(user, category):
    return Post.objects.create(
        title="Test Post",
        slug="test-post",
        content="Test content",
        author=user,
        category=category,
        status="draft",
    )


@pytest.mark.django_db
class TestPostAPI:
    def test_list_posts(self, api_client):
        response = api_client.get("/api/posts/")
        assert response.status_code == status.HTTP_200_OK

    def test_create_post(self, api_client, user, category):
        api_client.force_authenticate(user=user)
        data = {
            "title": "New Test Post",
            "content": "New test content",
            "author_id": user.id,
            "category_id": category.id,
            "status": "draft",
        }
        response = api_client.post("/api/posts/", data)
        assert response.status_code == status.HTTP_201_CREATED
        assert Post.objects.filter(title="New Test Post").exists()

    def test_schedule_post(self, api_client, user, category):
        api_client.force_authenticate(user=user)
        scheduled_date = timezone.now() + timedelta(days=1)
        data = {
            "title": "Scheduled Post",
            "content": "This will be published later",
            "author_id": user.id,
            "category_id": category.id,
            "status": "scheduled",
            "scheduled_date": scheduled_date.isoformat(),
        }
        response = api_client.post("/api/posts/", data)
        assert response.status_code == status.HTTP_201_CREATED
        post = Post.objects.get(title="Scheduled Post")
        assert post.status == "scheduled"
        assert post.scheduled_date.date() == scheduled_date.date()


@pytest.mark.django_db
class TestCategoryAPI:
    def test_list_categories(self, api_client):
        response = api_client.get("/api/categories/")
        assert response.status_code == status.HTTP_200_OK

    def test_create_category(self, api_client, user):
        api_client.force_authenticate(user=user)
        data = {"name": "New Category", "description": "Test description"}
        response = api_client.post("/api/categories/", data)
        assert response.status_code == status.HTTP_201_CREATED
        assert Category.objects.filter(name="New Category").exists()


@pytest.mark.django_db
class TestSchedulePostTask:
    def test_schedule_post_publication(self, post):
        post.status = "scheduled"
        post.scheduled_date = timezone.now() - timedelta(minutes=1)
        post.save()

        result = schedule_post_publication(post.id)
        post.refresh_from_db()

        assert post.status == "published"
        assert "Successfully published" in result
        assert post.published_date is not None
