import uuid
from django.db import models

class Activity(models.Model):
    TYPE_CHOICES = (
        ("github", "GitHub"),
        ("project", "Project"),
        ("learning", "Learning"),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    link = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title