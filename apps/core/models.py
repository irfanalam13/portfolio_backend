import uuid
from django.db import models


class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


# 🔥 SEO MODEL
class SEO(BaseModel):
    title = models.CharField(max_length=255)
    description = models.TextField()
    keywords = models.CharField(max_length=500, blank=True)
    og_image = models.ImageField(upload_to="seo/", blank=True, null=True)

    def __str__(self):
        return self.title


# 🔥 HERO IMAGE (SINGLE USE)
class HeroImage(BaseModel):
    image = models.ImageField(upload_to="hero/")
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.image.name.split("/")[-1]


# 🔥 HERO CONTENT
class HeroContent(BaseModel):
    headline = models.CharField(max_length=255)
    subheadline = models.CharField(max_length=255)

    cta_text = models.CharField(max_length=100, default="View My Work")
    cta_link = models.CharField(max_length=255, default="/projects")

    def __str__(self):
        return self.headline


# 🔥 HOMEPAGE (ONLY ONE IMAGE)
class HomePage(BaseModel):
    hero = models.ForeignKey(HeroContent, on_delete=models.SET_NULL, null=True)
    seo = models.ForeignKey(SEO, on_delete=models.SET_NULL, null=True)

    # ✅ Only ONE image allowed
    hero_image = models.ForeignKey(
        HeroImage,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    def __str__(self):
        return "Homepage"
    