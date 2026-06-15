# apps/contact/views.py
from rest_framework import mixins, viewsets
from rest_framework.throttling import ScopedRateThrottle

from .models import Contact
from .serializers import ContactSerializer


class ContactViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """Public contact form.

    Create-only: list / retrieve / update / delete are intentionally NOT
    exposed (the previous ModelViewSet allowed anyone to read or delete every
    submission). Rate limited per client IP to deter spam/abuse.
    """

    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "contact"
