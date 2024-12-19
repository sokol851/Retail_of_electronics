from rest_framework import viewsets
from rest_framework.filters import SearchFilter

from employees.permissions import IsActiveAuthenticated
from relations.models import Partner
from relations.serializers import PartnerSerializer


class PartnerViewSet(viewsets.ModelViewSet):
    serializer_class = PartnerSerializer
    queryset = Partner.objects.all()
    permission_classes = [IsActiveAuthenticated]
    filter_backends = [SearchFilter]
    search_fields = ['contact__country', ]
