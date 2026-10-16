import uuid
from django.db import models
from cloudinary.models import CloudinaryField


# 🔥 BASE MODEL (Reusable)
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

    og_image = CloudinaryField(
        'image',
        folder='portfolio/seo',
        blank=True,
        null=True
    )

    def __str__(self):
        return self.title


# 🔥 HERO BACKGROUND IMAGES (MULTIPLE)
class HeroBackground(BaseModel):
    image = CloudinaryField(
        'image',
        folder='portfolio/hero/background'
    )

    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0)

    def __str__(self):
        return f"Background {self.id}"


# 🔥 PROFILE IMAGE (SINGLE USE)
class ProfileImage(BaseModel):
    image = CloudinaryField(
        'image',
        folder='portfolio/hero/profile'
    )

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Profile {self.id}"


# 🔥 HERO CONTENT
class HeroContent(BaseModel):
    headline = models.CharField(max_length=255)
    subheadline = models.CharField(max_length=255)

    cta_text = models.CharField(max_length=100, default="View My Work")
    cta_link = models.CharField(max_length=255, default="/projects")

    def __str__(self):
        return self.headline


# 🔥 HOMEPAGE CONFIG (MAIN CONTROL)
class HomePage(BaseModel):
    hero = models.ForeignKey(
        HeroContent,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    seo = models.ForeignKey(
        SEO,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    profile_image = models.ForeignKey(
        ProfileImage,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    def __str__(self):
        return "Homepage"


class SiteProfile(models.Model):
    id = models.PositiveSmallIntegerField(primary_key=True, default=1, editable=False)
    name = models.CharField(max_length=255)
    username = models.CharField(max_length=100, blank=True)
    title = models.CharField(max_length=255)
    headline = models.TextField(blank=True)
    description = models.TextField(blank=True)
    location = models.CharField(max_length=255, blank=True)
    availability_status = models.BooleanField(default=False)
    availability_text = models.CharField(max_length=255, blank=True)
    resume_url = models.CharField(max_length=500, blank=True)
    profile_image_url = models.CharField(max_length=500, blank=True)

    def __str__(self):
        return self.name


class SummaryStat(models.Model):
    title = models.CharField(max_length=255)
    value = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return self.title


class Service(models.Model):
    slug = models.SlugField(unique=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    icon = models.CharField(max_length=100, blank=True)
    technologies = models.JSONField(default=list, blank=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order", "title"]

    def __str__(self):
        return self.title


class NavigationLink(models.Model):
    label = models.CharField(max_length=100)
    href = models.CharField(max_length=500)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return self.label


class SocialLink(models.Model):
    name = models.CharField(max_length=100)
    url = models.URLField(max_length=500, blank=True)
    icon = models.CharField(max_length=100, blank=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order", "name"]

    def __str__(self):
        return self.name