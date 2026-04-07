import uuid
from django.db import models

class SkillCategory(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Skill(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    level = models.IntegerField(help_text="0 to 100")
    category = models.ForeignKey(SkillCategory, on_delete=models.CASCADE, related_name="skills")

    def __str__(self):
        return self.name