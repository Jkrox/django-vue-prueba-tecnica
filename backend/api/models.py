from django.contrib.auth.models import User
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name


class Post(models.Model):
    STATUS_CHOICES = [
        ("draft", "Draft"),
        ("scheduled", "Scheduled"),
        ("published", "Published"),
    ]

    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    content = models.TextField()
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, related_name="posts"
    )
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="draft")
    published_date = models.DateTimeField(null=True, blank=True)
    scheduled_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    views = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_approved = models.BooleanField(default=False)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Comment by {self.author.username} on {self.post.title}"


class Tag(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True)
    posts = models.ManyToManyField(Post, related_name="tags")

    def __str__(self):
        return self.name
