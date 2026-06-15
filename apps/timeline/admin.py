from django.contrib import admin
from .models import TimelineEvent

@admin.register(TimelineEvent)
class TimelineAdmin(admin.ModelAdmin):
    list_display = ("title", "event_type", "start_date", "is_current")
    list_filter = ("event_type", "is_current")
    