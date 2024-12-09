import django_filters
from .models import Accommodation, Institution, PropertyType, Amenity, PaymentMethod


class AccommodationFilter(django_filters.FilterSet):
    city = django_filters.CharFilter(field_name="city", lookup_expr="icontains")
    province = django_filters.CharFilter(field_name="province", lookup_expr="icontains")
    property_type = django_filters.ModelChoiceFilter(
        queryset=PropertyType.objects.all()
    )
    educational_institutions = django_filters.ModelMultipleChoiceFilter(
        queryset=Institution.objects.all(),
        field_name="educational_institutions__name",
        to_field_name="name",
    )
    payment_methods = django_filters.ModelMultipleChoiceFilter(
        queryset=PaymentMethod.objects.all(),
        field_name="accepted_payments__name",
        to_field_name="name",
    )
    amenities = django_filters.ModelMultipleChoiceFilter(
        queryset=Amenity.objects.all(),
        field_name="amenities__name",
        to_field_name="name",
    )
    gender_restriction = django_filters.ChoiceFilter(
        choices=[("any", "Any"), ("male", "Male"), ("female", "Female")]
    )
    monthly_rent = django_filters.RangeFilter()
    bathrooms = django_filters.RangeFilter()
    is_available = django_filters.BooleanFilter()
    furnished = django_filters.BooleanFilter()
    available_from = django_filters.DateFilter(
        field_name="available_from", lookup_expr="gte"
    )
    minimum_lease_period = django_filters.NumberFilter(
        field_name="minimum_lease_period", lookup_expr="lte"
    )

    class Meta:
        model = Accommodation
        fields = [
            "city",
            "province",
            "property_type",
            "educational_institutions",
            "amenities",
            "gender_restriction",
            "monthly_rent",
            "bathrooms",
            "is_available",
            "furnished",
            "available_from",
            "minimum_lease_period",
        ]
