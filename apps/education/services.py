from .models import Education


def create_education(data):
    return Education.objects.create(**data)
