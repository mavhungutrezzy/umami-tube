from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse

class CustomUser(AbstractUser):
    youtube_channel_id = models.CharField(max_length=255, unique=True, blank=True, null=True)
    channel_name = models.CharField(max_length=255, blank=True)
    channel_logo_url = models.URLField(blank=True)
    channel_banner_url = models.URLField(blank=True)
    bio = models.TextField(blank=True)
    is_creator = models.BooleanField(default=False)

    def __str__(self):
        return self.email

    def get_absolute_url(self):
        return reverse('creator_detail', kwargs={'username': self.username})