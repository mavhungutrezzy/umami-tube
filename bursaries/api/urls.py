from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    BursaryListView,
    BursaryDetailView,
    BursaryManagementViewSet,
    FieldOfStudyListView,
    StudyLevelListView,
    EducationLevelListView,
)

router = DefaultRouter()
router.register(r"", BursaryManagementViewSet, basename="bursary")

urlpatterns = [
    path("", BursaryListView.as_view(), name="bursary-list"),
    path("<slug:slug>/", BursaryDetailView.as_view(), name="bursary-detail"),
    path(
        "fields-of-study/", FieldOfStudyListView.as_view(), name="field-of-study-list"
    ),
    path("study-levels/", StudyLevelListView.as_view(), name="study-level-list"),
    path(
        "education-levels/",
        EducationLevelListView.as_view(),
        name="education-level-list",
    ),
    path("", include(router.urls)),
]

app_name = "bursaries"
