from django.db import models


class Education(models.Model):
    DEGREE_TYPES = (
        ("school", "School"),
        ("college", "College"),
        ("bachelor", "Bachelor"),
        ("master", "Master"),
        ("phd", "PhD"),
        ("course", "Course"),
    )

    title = models.CharField(max_length=255)
    institution = models.CharField(max_length=255)
    degree_type = models.CharField(max_length=20, choices=DEGREE_TYPES)
    
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)

    description = models.TextField(blank=True)
    grade = models.CharField(max_length=50, blank=True)

    logo = models.ImageField(upload_to="education/logos/", null=True, blank=True)

    is_current = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["order", "-start_date"]

    def __str__(self):
        return f"{self.title} - {self.institution}"






