from django.contrib import admin
from .models import Skill, SkillCategory


@admin.register(SkillCategory)
class SkillCategoryAdmin(admin.ModelAdmin):
	search_fields = ["name"]


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
	list_display = ["name", "category", "level_label", "level"]
	list_filter = ["category", "level_label"]
	search_fields = ["name", "category__name"]
from django.contrib import admin

# Register your models here.
