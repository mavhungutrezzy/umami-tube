from rest_framework import viewsets, permissions, generics, status
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from ..models import Bursary, FieldOfStudy, StudyLevel, EducationLevel
from .serializers import (
    BursaryListSerializer,
    BursaryDetailSerializer,
    BursaryCreateUpdateSerializer,
    FieldOfStudySerializer,
    StudyLevelSerializer,
    EducationLevelSerializer,
)
from ..filters import BursaryFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters


class FieldOfStudyListView(generics.ListAPIView):
    queryset = FieldOfStudy.objects.all()
    serializer_class = FieldOfStudySerializer
    permission_classes = [permissions.AllowAny]

    @method_decorator(cache_page(60 * 60))  # Cache for 1 hour
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class StudyLevelListView(generics.ListAPIView):
    queryset = StudyLevel.objects.all()
    serializer_class = StudyLevelSerializer
    permission_classes = [permissions.AllowAny]

    @method_decorator(cache_page(60 * 60))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class EducationLevelListView(generics.ListAPIView):
    queryset = EducationLevel.objects.all()
    serializer_class = EducationLevelSerializer
    permission_classes = [permissions.AllowAny]

    @method_decorator(cache_page(60 * 60))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


@extend_schema(tags=["Bursaries"])
class BursaryListView(generics.ListAPIView):
    queryset = Bursary.objects.select_related().prefetch_related(
        "fields_of_study", "education_levels", "study_levels"
    )
    serializer_class = BursaryListSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_class = BursaryFilter
    search_fields = ["name", "provider", "content"]
    ordering_fields = ["created_at", "application_deadline"]
    ordering = ["-created_at"]

    @method_decorator(cache_page(60 * 5))  # Cache for 5 minutes
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


@extend_schema(tags=["Bursaries"])
class BursaryDetailView(generics.RetrieveAPIView):
    queryset = Bursary.objects.select_related().prefetch_related(
        "fields_of_study", "education_levels", "study_levels"
    )
    serializer_class = BursaryDetailSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = "slug"

    @method_decorator(cache_page(60 * 5))
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)


@extend_schema(tags=["Bursary Management"])
class BursaryManagementViewSet(viewsets.ModelViewSet):
    serializer_class = BursaryCreateUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = "slug"
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_class = BursaryFilter
    search_fields = ["name", "provider", "content"]
    ordering_fields = ["created_at", "application_deadline"]
    ordering = ["-created_at"]

    def get_queryset(self):
        return Bursary.objects.select_related().prefetch_related(
            "fields_of_study", "education_levels", "study_levels"
        )

    def get_serializer_class(self):
        if self.action == "list":
            return BursaryListSerializer
        elif self.action == "retrieve":
            return BursaryDetailSerializer
        return BursaryCreateUpdateSerializer


@extend_schema(tags=["Provider Bursaries"])
class ProviderBursaryViewSet(viewsets.ModelViewSet):
    """
    Manage provider's bursaries.

    Requires authentication. Providers can only manage their own bursaries.
    """

    serializer_class = BursaryCreateUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = "slug"

    def get_queryset(self):
        return (
            Bursary.objects.select_related("owner")
            .prefetch_related("study_fields", "requirements", "universities")
            .filter(owner=self.request.user)
        )

    def get_serializer_class(self):
        if self.action == "list":
            return BursaryListSerializer
        elif self.action == "retrieve":
            return BursaryDetailSerializer
        return BursaryCreateUpdateSerializer

    @extend_schema(
        description="Create a new bursary listing",
        responses={201: BursaryDetailSerializer},
    )
    def create(self, request, *args, **kwargs):
        """Create a new bursary listing."""
        return super().create(request, *args, **kwargs)

    @extend_schema(
        description="Update a bursary listing", responses={200: BursaryDetailSerializer}
    )
    def update(self, request, *args, **kwargs):
        """Update a bursary listing."""
        instance = self.get_object()
        if instance.owner != request.user:
            return Response(
                {"error": "You don't have permission to edit this bursary"},
                status=status.HTTP_403_FORBIDDEN,
            )
        return super().update(request, *args, **kwargs)

    @extend_schema(description="Delete a bursary listing", responses={204: None})
    def destroy(self, request, *args, **kwargs):
        """Delete a bursary listing."""
        instance = self.get_object()
        if instance.owner != request.user:
            return Response(
                {"error": "You don't have permission to delete this bursary"},
                status=status.HTTP_403_FORBIDDEN,
            )
        return super().destroy(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
