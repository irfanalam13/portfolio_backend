import uuid
from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify

User = get_user_model()

class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Tag(BaseModel):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Problem(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)

    description = models.TextField()
    tags = models.ManyToManyField(Tag, blank=True)

    views = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Answer(BaseModel):
    problem = models.ForeignKey(Problem, related_name="answers", on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    content = models.TextField()
    is_accepted = models.BooleanField(default=False)

    upvotes = models.IntegerField(default=0)

    def __str__(self):
        return f"Answer to {self.problem.title}"