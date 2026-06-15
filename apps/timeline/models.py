from django.db import models

class TimelineEvent(models.Model):
    EVENT_TYPES = (
        ("project", "Project"),
        ("experience", "Experience"),
        ("achievement", "Achievement"),
        ("education", "Education"),
    )

    title = models.CharField(max_length=255)
    description = models.TextField()
    event_type = models.CharField(max_length=20, choices=EVENT_TYPES)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)

    company = models.CharField(max_length=255, blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)

    image = models.ImageField(upload_to="timeline/", blank=True, null=True)
    is_current = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-start_date"]

    def __str__(self):
        return self.title
    