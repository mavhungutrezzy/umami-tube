from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    InstitutionListView,
    PropertyTypeListView,
    PaymentMethodListView,
    AmenityListView,
    AccommodationListView,
    AccommodationDetailView,
    LandlordAccommodationViewSet,
)

# Create a router for landlord accommodation viewset
router = DefaultRouter()
router.register(
    r"landlord/accommodations",
    LandlordAccommodationViewSet,
    basename="landlord-accommodation",
)

urlpatterns = [
    # Public Metadata Endpoints
    path("institutions/", InstitutionListView.as_view(), name="Institution-list"),
    path("property-types/", PropertyTypeListView.as_view(), name="property-type-list"),
    path(
        "payment-methods/", PaymentMethodListView.as_view(), name="payment-method-list"
    ),
    path("amenities/", AmenityListView.as_view(), name="amenity-list"),
    # Public Accommodation Endpoints
    path("accommodations/", AccommodationListView.as_view(), name="accommodation-list"),
    path(
        "accommodations/<slug:slug>/",
        AccommodationDetailView.as_view(),
        name="accommodation-detail",
    ),
    # Landlord Accommodation Endpoints
    path("", include(router.urls)),
]
