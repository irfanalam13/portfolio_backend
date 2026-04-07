import uuid
from django.db import models
from django.utils.text import slugify

class Project(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # Basic Info
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)

    short_description = models.TextField()
    full_description = models.TextField()

    # Links
    live_url = models.URLField(blank=True, null=True)
    github_url = models.URLField(blank=True, null=True)

    # SEO
    meta_title = models.CharField(max_length=255, blank=True)
    meta_description = models.TextField(blank=True)

    # Media
    thumbnail = models.ImageField(upload_to='projects/')
    featured = models.BooleanField(default=False)

    # Dates
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)

        if not self.meta_title:
            self.meta_title = self.title

        if not self.meta_description:
            self.meta_description = self.short_description[:150]

        super().save(*args, **kwargs)

    def __str__(self):
        return self.title