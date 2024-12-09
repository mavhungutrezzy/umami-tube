from django.db import models
from django.utils.text import slugify
from django_ckeditor_5.fields import CKEditor5Field


class FieldOfStudy(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "Fields of Study"

    def __str__(self):
        return self.name


class StudyLevel(models.Model):
    LEVEL_CHOICES = [
        ("certificate", "Certificate"),
        ("diploma", "Diploma"),
        ("degree", "Degree"),
        ("honours", "Honours"),
        ("masters", "Masters"),
        ("phd", "PhD"),
    ]

    name = models.CharField(max_length=50, choices=LEVEL_CHOICES)

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "Study Levels"

    def __str__(self):
        return self.get_name_display()


class EducationLevel(models.Model):
    LEVEL_CHOICES = [
        ("undergraduate", "Undergraduate"),
        ("postgraduate", "Postgraduate"),
    ]

    name = models.CharField(max_length=50, choices=LEVEL_CHOICES)

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "Education Levels"

    def __str__(self):
        return self.get_name_display()


class Bursary(models.Model):
    STATUS_CHOICES = [
        ("open", "Open"),
        ("closed", "Closed"),
        ("upcoming", "Upcoming"),
    ]

    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    provider = models.CharField(max_length=200)
    content = CKEditor5Field("Text")
    application_url = models.URLField(blank=True)
    application_deadline = models.DateField(null=True, blank=True)
    academic_year = models.CharField(max_length=4, db_index=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="open")

    fields_of_study = models.ManyToManyField(FieldOfStudy, related_name="bursaries")
    education_levels = models.ManyToManyField(EducationLevel, related_name="bursaries")
    study_levels = models.ManyToManyField(StudyLevel, related_name="bursaries")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name_plural = "Bursaries"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
