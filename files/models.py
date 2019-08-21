import uuid
from datetime import timedelta

from django.db import models
from django.urls import reverse
from django.utils import timezone


def tomorrow():
    return timezone.now() + timedelta(days=1)


class TimestampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class HiddenMixIn(TimestampedModel):
    slug = models.SlugField(max_length=64, default=uuid.uuid1, unique=True)
    expires_at = models.DateTimeField(default=tomorrow)
    click_count = models.IntegerField(default=0)
    password = models.CharField(max_length=120)


class FileHolder(HiddenMixIn):
    file = models.FileField()

    def get_absolute_url(self):
        return reverse('files-detail', args=[str(self.slug)])


class UrlHolder(HiddenMixIn):
    url = models.URLField()

    def get_absolute_url(self):
        return reverse('urls-detail', args=[str(self.slug)])
