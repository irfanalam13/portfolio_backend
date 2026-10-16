# apps/contact/models.py
from django.db import models
from apps.core.models import BaseModel

class Contact(BaseModel):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()