import json
from datetime import date
from pathlib import Path
from urllib.parse import urlparse

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.utils.text import slugify

from apps.achievements.models import Certification
from apps.core.models import NavigationLink, Service, SiteProfile, SocialLink, SummaryStat
from apps.education.models import Education
from apps.experience.models import Experience
from apps.projects.models import Project
from apps.skills.models import Skill, SkillCategory


class Command(BaseCommand):
    help = "Import portfolio section JSON into the database (repeatable; never deletes rows)."

    def add_arguments(self, parser):
        parser.add_argument(
            "--data-dir",
            type=Path,
            help="Directory containing section JSON files; defaults to frontend/src/data when available.",
        )
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Validate and report the import without connecting to the database.",
        )

    def handle(self, *args, **options):
        data = self.load_data(options["data_dir"])
        if options["dry_run"]:
            counts = self.validate_data(data)
            self.stdout.write(self.style.SUCCESS(f"Validated portfolio sections (no database changes): {counts}"))
            return
        try:
            self.validate_data(data)
            with transaction.atomic():
                counts = self.import_data(data)
        except (KeyError, TypeError, ValueError) as exc:
            raise CommandError(f"Invalid portfolio data: {exc}") from exc

        self.stdout.write(self.style.SUCCESS(f"Imported portfolio sections: {counts}"))

    def load_data(self, data_dir):
        if data_dir:
            return self.load_section_files(data_dir)

        frontend_data = settings.BASE_DIR.parent / "frontend" / "src" / "data"
        if frontend_data.is_dir():
            return self.load_section_files(frontend_data)

        bundled = Path(__file__).resolve().parents[2] / "seed_data" / "portfolio-seed.json"
        try:
            return json.loads(bundled.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            raise CommandError(f"Could not read bundled seed data at {bundled}: {exc}") from exc

    def load_section_files(self, data_dir):
        aliases = {
            "about": "about.json",
            "projects": "projects.json",
            "skills": "skills.json",
            "experience": "experience.json",
            "education": "education.json",
            "summary_stats": "achievement.json",
            "certifications": "certifications.json",
            "navigation": "navigations.json",
            "services": "services.json",
            "social_links": "social-link.json",
        }
        result = {}
        for section, filename in aliases.items():
            path = data_dir / filename
            if not path.exists():
                continue
            try:
                result[section] = json.loads(path.read_text(encoding="utf-8"))
            except json.JSONDecodeError as exc:
                raise CommandError(f"Invalid JSON in {path}: {exc}") from exc
        if not result:
            raise CommandError(f"No recognized section JSON files found in {data_dir}")
        return result

    def import_data(self, data):
        counts = {}
        if "about" in data:
            profile = data["about"]
            availability = profile.get("availability") or {}
            SiteProfile.objects.update_or_create(
                pk=1,
                defaults={
                    "name": profile["name"],
                    "username": profile.get("username", ""),
                    "title": profile.get("title", ""),
                    "headline": profile.get("headline", ""),
                    "description": profile.get("description", ""),
                    "location": profile.get("location", ""),
                    "availability_status": bool(availability.get("status", False)),
                    "availability_text": availability.get("text", ""),
                    "resume_url": profile.get("resume", ""),
                    "profile_image_url": profile.get("profileImage", ""),
                },
            )
            counts["profile"] = 1

        for item in data.get("projects", []):
            title = item["title"]
            slug = item.get("slug") or slugify(title)
            description = item.get("short_description") or item.get("description", "")
            full_description = item.get("full_description") or item.get("description", "") or description
            raw_case_study = item.get("case_study") or {}
            Project.objects.update_or_create(
                slug=slug,
                defaults={
                    "title": title,
                    "short_description": description,
                    "full_description": full_description,
                    "live_url": item.get("live_url") or item.get("live") or None,
                    "github_url": item.get("github_url") or item.get("github") or None,
                    "meta_title": item.get("meta_title", ""),
                    "meta_description": item.get("meta_description", ""),
                    "thumbnail_url": item.get("thumbnail") or item.get("image", ""),
                    "featured": bool(item.get("featured", False)),
                    "technologies": item.get("technologies", []),
                    "category": item.get("category", ""),
                    "features": item.get("features", []),
                    "status": item.get("status", ""),
                    "case_study": {
                        "problem": raw_case_study.get("problem", ""),
                        "solution": raw_case_study.get("solution", ""),
                        "result": raw_case_study.get("result", ""),
                    },
                },
            )
        if "projects" in data:
            counts["projects"] = len(data["projects"])

        for category_name, skills in (data.get("skills") or {}).items():
            category_name = self.category_label(category_name)
            category = SkillCategory.objects.filter(name=category_name).first()
            if category is None:
                category = SkillCategory.objects.create(name=category_name)
            for item in skills:
                label = str(item.get("level", "Intermediate"))
                level = {"beginner": 35, "intermediate": 65, "advanced": 90}.get(label.lower(), 65)
                Skill.objects.update_or_create(
                    name=item["name"], category=category,
                    defaults={"level": level, "level_label": label},
                )
        if "skills" in data:
            counts["skills"] = sum(len(items) for items in data["skills"].values())

        for item in data.get("experience", []):
            start_date = self.year_date(item.get("startDate") or item.get("start_date"))
            end_raw = item.get("endDate") or item.get("end_date")
            is_current = str(end_raw or "").lower() in {"present", "current", "now"} or not end_raw
            Experience.objects.update_or_create(
                company=item["company"], role=item.get("position") or item.get("role", ""), start_date=start_date,
                defaults={
                    "description": item.get("description", ""),
                    "end_date": None if is_current else self.year_date(end_raw),
                    "is_current": is_current,
                    "employment_type": item.get("type", ""),
                    "location": item.get("location", ""),
                    "technologies": item.get("technologies", []),
                },
            )
        if "experience" in data:
            counts["experience"] = len(data["experience"])

        for index, item in enumerate(data.get("education", [])):
            start_date = self.year_date(item.get("startYear") or item.get("start_date"))
            end_raw = item.get("endYear") or item.get("end_date")
            is_current = bool(item.get("is_current")) or not end_raw or str(end_raw).lower() in {"present", "current"}
            degree = item.get("degree", item.get("title", ""))
            degree_type = self.degree_type(degree)
            Education.objects.update_or_create(
                institution=item["institution"], title=degree, start_date=start_date,
                defaults={
                    "degree_type": degree_type,
                    "end_date": None if is_current else self.year_date(end_raw),
                    "description": item.get("description", ""),
                    "field_of_study": item.get("field", ""),
                    "location": item.get("location", ""),
                    "is_current": is_current,
                    "order": index,
                },
            )
        if "education" in data:
            counts["education"] = len(data["education"])

        for index, item in enumerate(data.get("summary_stats", [])):
            SummaryStat.objects.update_or_create(
                title=item["title"], defaults={"value": str(item["value"]), "description": item.get("description", ""), "order": index}
            )
        if "summary_stats" in data:
            counts["summary_stats"] = len(data["summary_stats"])

        for item in data.get("certifications", []):
            raw_year = item.get("issueDate") or item.get("issue_date")
            year = self.year_number(raw_year)
            Certification.objects.update_or_create(
                name=item["name"], organization=item.get("issuer") or item.get("organization", ""),
                defaults={
                    "issue_date": date(year, 1, 1) if year else None,
                    "issue_year": year,
                    "credential_id": item.get("credentialId") or item.get("credential_id", ""),
                    "credential_url": item.get("credentialUrl") or item.get("credential_url", ""),
                    "image_url": item.get("image", ""),
                },
            )
        if "certifications" in data:
            counts["certifications"] = len(data["certifications"])

        for index, item in enumerate(data.get("services", [])):
            slug = item.get("id") or slugify(item["title"])
            Service.objects.update_or_create(
                slug=slug,
                defaults={"title": item["title"], "description": item["description"], "icon": item.get("icon", ""), "technologies": item.get("technologies", []), "order": index, "is_active": True},
            )
        if "services" in data:
            counts["services"] = len(data["services"])

        for index, item in enumerate(data.get("navigation", [])):
            NavigationLink.objects.update_or_create(
                href=item["href"], defaults={"label": item.get("label", item.get("name", "")), "order": index, "is_active": True}
            )
        if "navigation" in data:
            counts["navigation"] = len(data["navigation"])

        for index, item in enumerate(data.get("social_links", [])):
            url = item.get("url", "")
            active = bool(url) and "yourusername" not in url.lower() and "yourusername" not in urlparse(url).path.lower()
            SocialLink.objects.update_or_create(
                name=item["name"], defaults={"url": url, "icon": item.get("icon", ""), "order": index, "is_active": active},
            )
        if "social_links" in data:
            counts["social_links"] = len(data["social_links"])

        return counts

    def validate_data(self, data):
        """Validate required keys, collection shapes, and date precision without database access."""
        if not isinstance(data, dict):
            raise CommandError("The data root must be a JSON object.")
        for key in ("projects", "experience", "education", "summary_stats", "certifications", "navigation", "services", "social_links"):
            if key in data and not isinstance(data[key], list):
                raise CommandError(f"Section '{key}' must be a JSON array.")
        if "about" in data:
            if not isinstance(data["about"], dict) or not data["about"].get("name"):
                raise CommandError("The about section must be an object with a name.")
        for item in data.get("projects", []):
            if not item.get("title"):
                raise CommandError("Every project requires a title.")
        for category, items in (data.get("skills") or {}).items():
            if not isinstance(items, list):
                raise CommandError(f"Skill category '{category}' must be an array.")
            for item in items:
                if not item.get("name"):
                    raise CommandError(f"Every skill in '{category}' requires a name.")
        for item in data.get("experience", []):
            if not item.get("company") or not (item.get("startDate") or item.get("start_date")):
                raise CommandError("Every experience record requires a company and start year/date.")
            self.year_date(item.get("startDate") or item.get("start_date"))
            end = item.get("endDate") or item.get("end_date")
            if end and str(end).lower() not in {"present", "current", "now"}:
                self.year_date(end)
        for item in data.get("education", []):
            if not item.get("institution") or not (item.get("startYear") or item.get("start_date")):
                raise CommandError("Every education record requires an institution and start year/date.")
            self.year_date(item.get("startYear") or item.get("start_date"))
            end = item.get("endYear") or item.get("end_date")
            if end:
                self.year_date(end)
        for item in data.get("certifications", []):
            if not item.get("name"):
                raise CommandError("Every certification requires a name.")
            year = item.get("issueDate") or item.get("issue_date")
            if year:
                self.year_number(year)
        for item in data.get("summary_stats", []):
            if not item.get("title") or "value" not in item:
                raise CommandError("Every summary stat requires a title and value.")
        for item in data.get("services", []):
            if not item.get("title") or not item.get("description"):
                raise CommandError("Every service requires a title and description.")
        for item in data.get("navigation", []):
            if not item.get("href"):
                raise CommandError("Every navigation item requires an href.")

        counts = {key: len(value) for key, value in data.items() if isinstance(value, list)}
        if "about" in data:
            counts["profile"] = 1
        if "skills" in data:
            counts["skills"] = sum(len(value) for value in data["skills"].values())
        return counts

    @staticmethod
    def category_label(value):
        if value.lower() == "ai_ml":
            return "AI & ML"
        return value.replace("_", " ").title()

    @staticmethod
    def year_number(value):
        if not value:
            return None
        text = str(value).strip()
        if text.isdigit() and len(text) == 4:
            return int(text)
        return date.fromisoformat(text[:10]).year

    @classmethod
    def year_date(cls, value):
        year = cls.year_number(value)
        return date(year, 1, 1) if year else None

    @staticmethod
    def degree_type(value):
        normalized = str(value).lower()
        if "ph.d" in normalized or "phd" in normalized:
            return "phd"
        if "master" in normalized:
            return "master"
        if "bachelor" in normalized or "b.sc" in normalized or "bachelor's" in normalized:
            return "bachelor"
        if "school" in normalized:
            return "school"
        if "course" in normalized or "certificate" in normalized:
            return "course"
        return "college"
