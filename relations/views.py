from rest_framework import viewsets
from rest_framework.filters import SearchFilter

from employees.permissions import IsActiveAuthenticated
from relations.models import Partner, Product
from relations.serializers import PartnerSerializer, ProductSerializer


class PartnerViewSet(viewsets.ModelViewSet):
    """ Представление для партнёра """
    serializer_class = PartnerSerializer
    queryset = Partner.objects.all()
    permission_classes = [IsActiveAuthenticated]
    filter_backends = [SearchFilter]
    search_fields = ['contact__country',
                     'contact__city',
                     'name',
                     'products__name']


class ProductViewSet(viewsets.ModelViewSet):
    """ Представление для продукта """
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    permission_classes = [IsActiveAuthenticated]
