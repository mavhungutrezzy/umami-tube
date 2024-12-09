from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django_filters.rest_framework import DjangoFilterBackend


from rest_framework import viewsets, generics, permissions, filters as drf_filters
from rest_framework.exceptions import PermissionDenied

from drf_spectacular.utils import extend_schema, OpenApiParameter

from ..models import Accommodation, Institution, PropertyType, PaymentMethod, Amenity
from .serializers import (
    AccommodationListSerializer,
    AccommodationDetailSerializer,
    AccommodationCreateUpdateSerializer,
    InstitutionSerializer,
    PropertyTypeSerializer,
    PaymentMethodSerializer,
    AmenitySerializer,
)
from ..filters import AccommodationFilter


class BaseListView(generics.ListAPIView):
    """
    Base class for list views with common configurations.
    """

    permission_classes = [permissions.AllowAny]

    @method_decorator(cache_page(60 * 15))
    def list(self, request, *args, **kwargs):
        """
        Cached list method with optional caching.
        """
        return super().list(request, *args, **kwargs)


class InstitutionListView(BaseListView):
    """
    List all unique educational institutions from accommodations.
    """

    @extend_schema(
        description="Retrieve list of unique educational institutions",
        tags=["Educational Institutions"],
    )
    def get_queryset(self):
        """
        Get distinct educational institutions.
        """
        return Institution.objects.distinct()

    serializer_class = InstitutionSerializer


class PropertyTypeListView(BaseListView):
    """
    List all unique property types from accommodations.
    """

    @extend_schema(
        description="Retrieve list of unique property types", tags=["Property Types"]
    )
    def get_queryset(self):
        """
        Get distinct property types.
        """
        return PropertyType.objects.distinct()

    serializer_class = PropertyTypeSerializer


class PaymentMethodListView(BaseListView):
    """
    List all unique payment methods from accommodations.
    """

    @extend_schema(
        description="Retrieve list of unique payment methods", tags=["Payment Methods"]
    )
    def get_queryset(self):
        """
        Get distinct payment methods.
        """
        return PaymentMethod.objects.distinct()

    serializer_class = PaymentMethodSerializer


class AmenityListView(BaseListView):
    """
    List all unique amenities from accommodations.
    """

    @extend_schema(description="Retrieve list of unique amenities", tags=["Amenities"])
    def get_queryset(self):
        """
        Get distinct amenities.
        """
        return Amenity.objects.distinct()

    serializer_class = AmenitySerializer


class AccommodationListView(generics.ListAPIView):
    """
    Comprehensive accommodation listing with advanced filtering.
    """

    queryset = (
        Accommodation.objects.select_related("property_type")
        .prefetch_related("educational_institutions", "amenities", "accepted_payments")
        .filter(is_available=True)
    )
    serializer_class = AccommodationListSerializer
    permission_classes = [permissions.AllowAny]
    filterset_class = AccommodationFilter

    filter_backends = [
        drf_filters.SearchFilter,
        drf_filters.OrderingFilter,
        DjangoFilterBackend,  # Use DjangoFilterBackend for compatibility
    ]

    search_fields = ["title", "description", "address", "city", "province"]
    ordering_fields = ["monthly_rent", "created_at"]
    ordering = ["-created_at"]

    @extend_schema(
        description="Search and filter accommodations",
        tags=["Public Accommodations"],
        parameters=[
            OpenApiParameter(
                name="search",
                description="Search across title, description, address",
                required=False,
            ),
            OpenApiParameter(
                name="min_rent", description="Minimum monthly rent", required=False
            ),
            OpenApiParameter(
                name="max_rent", description="Maximum monthly rent", required=False
            ),
        ],
    )
    @method_decorator(cache_page(60 * 15))
    def list(self, request, *args, **kwargs):
        """
        Cached list method with advanced filtering.
        """
        return super().list(request, *args, **kwargs)


class AccommodationDetailView(generics.RetrieveAPIView):
    """
    Retrieve detailed information about a specific accommodation.
    """

    queryset = Accommodation.objects.select_related("property_type").prefetch_related(
        "educational_institutions", "amenities", "accepted_payments"
    )
    serializer_class = AccommodationDetailSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = "slug"

    @method_decorator(cache_page(60 * 15))
    @extend_schema(
        description="Get detailed accommodation information",
        tags=["Public Accommodations"],
    )
    def retrieve(self, request, *args, **kwargs):
        """
        Cached detail retrieval with performance optimizations.
        """
        return super().retrieve(request, *args, **kwargs)


class LandlordAccommodationViewSet(viewsets.ModelViewSet):
    """
    Comprehensive management of landlord accommodations.
    """

    permission_classes = [permissions.IsAuthenticated]
    lookup_field = "slug"

    def get_queryset(self):
        """
        Get accommodations owned by the current user.
        """
        return (
            Accommodation.objects.select_related("property_type")
            .prefetch_related(
                "educational_institutions", "amenities", "accepted_payments"
            )
            .filter(owner=self.request.user)
        )

    def get_serializer_class(self):
        """
        Dynamic serializer selection based on action.
        """
        action_serializers = {
            "list": AccommodationListSerializer,
            "retrieve": AccommodationDetailSerializer,
        }
        return action_serializers.get(self.action, AccommodationCreateUpdateSerializer)

    def check_object_permissions(self, request, obj):
        """
        Enhanced permission checking for object-level operations.
        """
        super().check_object_permissions(request, obj)

        if obj.owner != request.user:
            raise PermissionDenied("You do not have permission to perform this action.")

    def perform_create(self, serializer):
        """
        Set the owner during accommodation creation.
        """
        serializer.save(owner=self.request.user)
