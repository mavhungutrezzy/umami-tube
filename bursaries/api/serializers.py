from rest_framework import serializers
from ..models import Bursary, FieldOfStudy, StudyLevel, EducationLevel


class FieldOfStudySerializer(serializers.ModelSerializer):
    class Meta:
        model = FieldOfStudy
        fields = ["id", "name"]


class StudyLevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudyLevel
        fields = ["id", "name"]


class EducationLevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = EducationLevel
        fields = ["id", "name"]


class BursaryListSerializer(serializers.ModelSerializer):
    fields_of_study = FieldOfStudySerializer(many=True, read_only=True)
    education_levels = EducationLevelSerializer(many=True, read_only=True)
    study_levels = StudyLevelSerializer(many=True, read_only=True)

    class Meta:
        model = Bursary
        fields = [
            "id",
            "name",
            "slug",
            "provider",
            "application_deadline",
            "academic_year",
            "status",
            "fields_of_study",
            "education_levels",
            "study_levels",
        ]


class BursaryDetailSerializer(serializers.ModelSerializer):
    fields_of_study = FieldOfStudySerializer(many=True, read_only=True)
    education_levels = EducationLevelSerializer(many=True, read_only=True)
    study_levels = StudyLevelSerializer(many=True, read_only=True)

    class Meta:
        model = Bursary
        fields = [
            "id",
            "name",
            "slug",
            "provider",
            "content",
            "application_url",
            "application_deadline",
            "academic_year",
            "status",
            "fields_of_study",
            "education_levels",
            "study_levels",
            "created_at",
            "updated_at",
        ]


class BursaryCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bursary
        fields = [
            "name",
            "provider",
            "content",
            "application_url",
            "application_deadline",
            "academic_year",
            "status",
            "fields_of_study",
            "education_levels",
            "study_levels",
        ]

    def validate_application_deadline(self, value):
        from django.utils import timezone

        if value and value < timezone.now().date():
            raise serializers.ValidationError(
                "Application deadline cannot be in the past"
            )
        return value
