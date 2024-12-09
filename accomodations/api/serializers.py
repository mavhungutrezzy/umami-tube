from rest_framework import serializers
from ..models import (
    Institution,
    PropertyType,
    PaymentMethod,
    Amenity,
    Accommodation,
)


class InstitutionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Institution
        fields = ["id", "name", "city", "province"]


class PropertyTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyType
        fields = ["id", "name", "description"]


class PaymentMethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentMethod
        fields = ["id", "name", "description"]


class AmenitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Amenity
        fields = ["id", "name", "description"]


class AccommodationListSerializer(serializers.ModelSerializer):
    property_type = PropertyTypeSerializer(read_only=True)
    educational_institutions = InstitutionSerializer(many=True, read_only=True)
    amenities = AmenitySerializer(many=True, read_only=True)

    class Meta:
        model = Accommodation
        fields = [
            "id",
            "title",
            "slug",
            "property_type",
            "educational_institutions",
            "city",
            "province",
            "monthly_rent",
            "max_occupants",
            "bathrooms",
            "furnished",
            "gender_restriction",
            "is_available",
            "is_verified",
            "available_from",
            "amenities",
            "created_at",
        ]


class AccommodationDetailSerializer(serializers.ModelSerializer):
    property_type = PropertyTypeSerializer(read_only=True)
    educational_institutions = InstitutionSerializer(many=True, read_only=True)
    amenities = AmenitySerializer(many=True, read_only=True)
    accepted_payments = PaymentMethodSerializer(many=True, read_only=True)

    class Meta:
        model = Accommodation
        fields = [
            "id",
            "title",
            "slug",
            "description",
            "property_type",
            "educational_institutions",
            "address",
            "city",
            "province",
            "postal_code",
            "monthly_rent",
            "deposit_amount",
            "max_occupants",
            "bathrooms",
            "furnished",
            "gender_restriction",
            "is_available",
            "is_verified",
            "available_from",
            "minimum_lease_period",
            "amenities",
            "accepted_payments",
            "contact_phone",
            "contact_email",
            "whatsapp",
            "website",
            "created_at",
            "updated_at",
        ]


class AccommodationCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Accommodation
        fields = [
            "title",
            "description",
            "property_type",
            "educational_institutions",
            "address",
            "city",
            "province",
            "postal_code",
            "monthly_rent",
            "deposit_amount",
            "max_occupants",
            "bathrooms",
            "furnished",
            "gender_restriction",
            "is_available",
            "available_from",
            "minimum_lease_period",
            "amenities",
            "accepted_payments",
            "contact_phone",
            "contact_email",
            "whatsapp",
            "website",
        ]

    def validate(self, data):
        """
        Comprehensive validation for accommodation data.
        """
        # Validate rent and deposit
        if data.get("monthly_rent", 0) <= 0:
            raise serializers.ValidationError(
                {"monthly_rent": "Rent must be a positive value."}
            )

        if data.get("deposit_amount", 0) < 0:
            raise serializers.ValidationError(
                {"deposit_amount": "Deposit cannot be negative."}
            )

        # Validate occupancy
        if data.get("max_occupants", 1) < 1:
            raise serializers.ValidationError(
                {"max_occupants": "At least one occupant is required."}
            )

        # Validate available from date
        from datetime import date

        available_from = data.get("available_from")
        if available_from and available_from < date.today():
            raise serializers.ValidationError(
                {"available_from": "Available date must be in the future."}
            )

        return data

    def create(self, validated_data):
        """
        Custom creation method with relationship handling.
        """
        # Remove many-to-many fields for initial creation
        educational_institutions = validated_data.pop("educational_institutions", [])
        amenities = validated_data.pop("amenities", [])
        accepted_payments = validated_data.pop("accepted_payments", [])

        # Create accommodation
        accommodation = Accommodation.objects.create(**validated_data)

        # Add many-to-many relationships
        if educational_institutions:
            accommodation.educational_institutions.set(educational_institutions)
        if amenities:
            accommodation.amenities.set(amenities)
        if accepted_payments:
            accommodation.accepted_payments.set(accepted_payments)

        return accommodation

    def update(self, instance, validated_data):
        """
        Custom update method with relationship handling.
        """
        # Handle many-to-many fields
        educational_institutions = validated_data.pop("educational_institutions", None)
        amenities = validated_data.pop("amenities", None)
        accepted_payments = validated_data.pop("accepted_payments", None)

        # Update instance attributes
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Update relationships if provided
        if educational_institutions is not None:
            instance.educational_institutions.set(educational_institutions)
        if amenities is not None:
            instance.amenities.set(amenities)
        if accepted_payments is not None:
            instance.accepted_payments.set(accepted_payments)

        return instance
