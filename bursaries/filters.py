import django_filters
from django.db.models import Q
from .models import Bursary


class BursaryFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr="icontains")
    provider = django_filters.CharFilter(lookup_expr="icontains")
    academic_year = django_filters.CharFilter(lookup_expr="exact")
    status = django_filters.ChoiceFilter(choices=Bursary.STATUS_CHOICES)
    
    # Date filters
    deadline_after = django_filters.DateFilter(
        field_name="application_deadline", lookup_expr="gte"
    )
    deadline_before = django_filters.DateFilter(
        field_name="application_deadline", lookup_expr="lte"
    )
    
    # Related field filters
    field_of_study = django_filters.CharFilter(
        field_name="fields_of_study__name", lookup_expr="iexact"
    )
    education_level = django_filters.CharFilter(
        field_name="education_levels__name", lookup_expr="iexact"
    )
    study_level = django_filters.CharFilter(
        field_name="study_levels__name", lookup_expr="iexact"
    )
    
    # Text search
    search = django_filters.CharFilter(method="filter_search")
    
    def filter_search(self, queryset, name, value):
        return queryset.filter(
            Q(name__icontains=value) |
            Q(provider__icontains=value) |
            Q(content__icontains=value)
        )

    class Meta:
        model = Bursary
        fields = [
            "name",
            "provider",
            "academic_year",
            "status",
            "field_of_study",
            "education_level",
            "study_level",
        ]