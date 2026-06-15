from django.db import models


class Achievement(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    issuer = models.CharField(max_length=255, blank=True)
    date = models.DateField(null=True, blank=True)
    link = models.URLField(blank=True)
    image = models.ImageField(upload_to="achievements/", null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Certification(models.Model):
    name = models.CharField(max_length=255)
    organization = models.CharField(max_length=255)
    issue_date = models.DateField()
    expiry_date = models.DateField(null=True, blank=True)
    credential_id = models.CharField(max_length=255, blank=True)
    credential_url = models.URLField(blank=True)
    image = models.ImageField(upload_to="certifications/", null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    