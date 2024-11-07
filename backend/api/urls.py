from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework.routers import DefaultRouter

from . import views

schema_view = get_schema_view(
    openapi.Info(
        title="Blog API",
        default_version="v1",
        description="API Documentation for Blog Platform",
        contact=openapi.Contact(email="contact@blogplatform.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
)

router = DefaultRouter()
router.register(r"categories", views.CategoryViewSet)
router.register(r"posts", views.PostViewSet, basename="post")
router.register(r"comments", views.CommentViewSet)
router.register(r"tags", views.TagViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
]
