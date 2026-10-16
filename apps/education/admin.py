from django.contrib import admin
from .models import Education 


@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = ("title", "institution", "degree_type", "start_date", "order")

