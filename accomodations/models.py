from django.db import models
from django.conf import settings
from django.utils.text import slugify
from .constants import (
    INSTITUTIONS,
    PROPERTY_TYPE_CHOICES,
    PAYMENT_TYPES,
    AMENITY_CHOICES,
    GENDER_CHOICES,
)


class Institution(models.Model):
    name = models.CharField(max_length=100, choices=INSTITUTIONS)
    city = models.CharField(max_length=100)
    province = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "educational institutions"
        ordering = ["name"]

    def __str__(self):
        return dict(INSTITUTIONS)[self.name]


class PropertyType(models.Model):
    name = models.CharField(max_length=50, choices=PROPERTY_TYPE_CHOICES, unique=True)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return dict(PROPERTY_TYPE_CHOICES)[self.name]


class PaymentMethod(models.Model):
    name = models.CharField(max_length=50, choices=PAYMENT_TYPES)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return dict(PAYMENT_TYPES)[self.name]


class Amenity(models.Model):
    name = models.CharField(max_length=100, choices=AMENITY_CHOICES, unique=True)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = "amenities"
        ordering = ["name"]

    def __str__(self):
        return dict(AMENITY_CHOICES)[self.name]


class Accommodation(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField()
    property_type = models.ForeignKey(PropertyType, on_delete=models.PROTECT)
    educational_institutions = models.ManyToManyField(
        Institution, related_name="accommodations"
    )
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    province = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=10)
    monthly_rent = models.DecimalField(max_digits=10, decimal_places=2)
    admin_fee = models.DecimalField(max_digits=10, decimal_places=2)
    deposit_amount = models.DecimalField(max_digits=10, decimal_places=2)
    max_occupants = models.PositiveIntegerField(default=1)
    bathrooms = models.DecimalField(max_digits=3, decimal_places=1)
    furnished = models.BooleanField(default=False)
    gender_restriction = models.CharField(
        max_length=10, choices=GENDER_CHOICES, default="any"
    )
    is_available = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)
    available_from = models.DateField()
    minimum_lease_period = models.PositiveIntegerField(
        help_text="Minimum lease period in months", default=12
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="accommodations",
    )
    amenities = models.ManyToManyField(Amenity, related_name="accommodations")
    accepted_payments = models.ManyToManyField(
        PaymentMethod, related_name="accommodations"
    )
    contact_phone = models.CharField(max_length=20)
    contact_email = models.EmailField()
    whatsapp = models.CharField(max_length=20, blank=True)
    website = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["city", "province"]),
            models.Index(fields=["is_available", "available_from"]),
            models.Index(fields=["monthly_rent"]),
        ]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} - {self.city}"

