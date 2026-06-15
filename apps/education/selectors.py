# apps/education/selectors.py

from .models import Education


def get_all_education():
    return Education.objects.all()   # ✅ clean & correct
