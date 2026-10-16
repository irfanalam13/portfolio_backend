from django.db import models

class Experience(models.Model):
    company = models.CharField(max_length=255)
    role = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)

    is_current = models.BooleanField(default=False)
    employment_type = models.CharField(max_length=100, blank=True)
    location = models.CharField(max_length=255, blank=True)
    technologies = models.JSONField(default=list, blank=True)

    company_logo = models.ImageField(upload_to="experience/logos/", null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.role} at {self.company}"
    