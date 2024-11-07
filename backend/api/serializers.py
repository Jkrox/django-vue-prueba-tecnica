from datetime import timezone

from django.contrib.auth.models import User
from django.utils.text import slugify
from rest_framework import serializers

from .models import Category, Comment, Post, Tag


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "first_name", "last_name"]


class CategorySerializer(serializers.ModelSerializer):
    slug = serializers.SlugField(read_only=True)
    posts_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Category
        fields = ["id", "name", "slug", "description", "created_at", "posts_count"]

    def create(self, validated_data):
        validated_data["slug"] = slugify(validated_data["name"])
        return super().create(validated_data)


class TagSerializer(serializers.ModelSerializer):
    slug = serializers.SlugField(read_only=True)

    class Meta:
        model = Tag
        fields = ["id", "name", "slug"]

    def create(self, validated_data):
        validated_data["slug"] = slugify(validated_data["name"])
        return super().create(validated_data)


class CommentSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    author_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Comment
        fields = [
            "id",
            "post",
            "author",
            "author_id",
            "content",
            "created_at",
            "updated_at",
            "is_approved",
        ]
        read_only_fields = ["created_at", "updated_at", "is_approved"]

    def validate_author_id(self, value):
        if not User.objects.filter(id=value).exists():
            raise serializers.ValidationError("Invalid author ID")
        return value


class PostSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    slug = serializers.SlugField(read_only=True)

    # Write-only fields for relations
    author_id = serializers.IntegerField(write_only=True)
    category_id = serializers.IntegerField(write_only=True, required=False)
    tag_ids = serializers.ListField(
        child=serializers.IntegerField(), write_only=True, required=False
    )

    class Meta:
        model = Post
        fields = [
            "id",
            "title",
            "slug",
            "author",
            "author_id",
            "content",
            "category",
            "category_id",
            "status",
            "published_date",
            "scheduled_date",
            "created_at",
            "updated_at",
            "views",
            "tags",
            "tag_ids",
            "comments",
        ]
        read_only_fields = ["created_at", "updated_at", "views", "slug"]

    def validate_scheduled_date(self, value):
        """
        Validate that scheduled date is in the future
        """
        if value and value < timezone.now():
            raise serializers.ValidationError("Scheduled date must be in the future")
        return value

    def validate(self, data):
        """
        Check that either published_date or scheduled_date is set when status
        is 'published' or 'scheduled'
        """
        if data.get("status") == "published" and not data.get("published_date"):
            data["published_date"] = timezone.now()
        elif data.get("status") == "scheduled" and not data.get("scheduled_date"):
            raise serializers.ValidationError(
                {"scheduled_date": "Scheduled date is required for scheduled posts"}
            )
        return data

    def create(self, validated_data):
        tag_ids = validated_data.pop("tag_ids", [])
        validated_data["slug"] = slugify(validated_data["title"])

        post = Post.objects.create(**validated_data)

        # Add tags
        if tag_ids:
            tags = Tag.objects.filter(id__in=tag_ids)
            post.tags.set(tags)

        return post

    def update(self, instance, validated_data):
        tag_ids = validated_data.pop("tag_ids", None)

        # Update the post instance
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        # Update slug if title changed
        if "title" in validated_data:
            instance.slug = slugify(validated_data["title"])

        instance.save()

        # Update tags if provided
        if tag_ids is not None:
            tags = Tag.objects.filter(id__in=tag_ids)
            instance.tags.set(tags)

        return instance


class PostListSerializer(PostSerializer):
    """
    Simplified serializer for list views
    """

    class Meta(PostSerializer.Meta):
        fields = [
            "id",
            "title",
            "slug",
            "author",
            "category",
            "status",
            "published_date",
            "views",
        ]
