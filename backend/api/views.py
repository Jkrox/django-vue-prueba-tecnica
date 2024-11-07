from django.db.models import Count
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from .models import Category, Comment, Post, Tag
from .serializers import (
    CategorySerializer,
    CommentSerializer,
    PostListSerializer,
    PostSerializer,
    TagSerializer,
)
from .tasks import schedule_post_publication


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.annotate(posts_count=Count("posts"))
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    lookup_field = "slug"
    filter_backends = [filters.SearchFilter]
    search_fields = ["name", "description"]


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    lookup_field = "slug"
    filter_backends = [filters.SearchFilter]
    search_fields = ["name"]


class PostViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    lookup_field = "slug"
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ["status", "category__slug", "author__username"]
    search_fields = ["title", "content"]
    ordering_fields = ["created_at", "published_date", "views"]
    ordering = ["-created_at"]

    def get_queryset(self):
        queryset = Post.objects.select_related("author", "category").prefetch_related(
            "tags", "comments"
        )
        if self.action == "list":
            return queryset.filter(
                status="published", published_date__lte=timezone.now()
            )
        return queryset

    def get_serializer_class(self):
        if self.action == "list":
            return PostListSerializer
        return PostSerializer

    def perform_create(self, serializer):
        post = serializer.save(author=self.request.user)
        if post.status == "scheduled" and post.scheduled_date:
            schedule_post_publication.apply_async(
                args=[post.id], eta=post.scheduled_date
            )

    @action(detail=True, methods=["post"])
    def toggle_status(self, request, slug=None):
        post = self.get_object()
        if post.status == "draft":
            post.status = "published"
            post.published_date = timezone.now()
        elif post.status == "published":
            post.status = "draft"
            post.published_date = None
        post.save()
        return Response(PostSerializer(post).data)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.select_related("author", "post")
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["post", "author", "is_approved"]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
