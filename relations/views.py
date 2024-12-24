from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import viewsets
from rest_framework.filters import SearchFilter

from employees.permissions import IsActiveAuthenticated
from relations.models import Partner, Product
from relations.serializers import PartnerSerializer, ProductSerializer


@extend_schema_view(
    list=extend_schema(summary="Получить список партнёров",
                       tags=["Партнёры"]),
    update=extend_schema(summary="Изменение партнёра",
                         tags=["Партнёры"]),
    retrieve=extend_schema(summary="Детализация партнёра",
                           tags=["Партнёры"]),
    partial_update=extend_schema(summary='Изменение части партнёра',
                                 tags=["Партнёры"]),
    create=extend_schema(summary="Создание партнёра",
                         tags=["Партнёры"]),
    destroy=extend_schema(summary="Удаление партнёра",
                          tags=["Партнёры"]),
)
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


@extend_schema_view(
    list=extend_schema(summary="Получить список продуктов",
                       tags=["Продукты"]),
    update=extend_schema(summary="Изменение продукта",
                         tags=["Продукты"]),
    retrieve=extend_schema(summary="Детализация продукта",
                           tags=["Продукты"]),
    partial_update=extend_schema(summary='Изменение части продукта',
                                 tags=["Продукты"]),
    create=extend_schema(summary="Создание продукта",
                         tags=["Продукты"]),
    destroy=extend_schema(summary="Удаление продукта",
                          tags=["Продукты"]),
)
class ProductViewSet(viewsets.ModelViewSet):
    """ Представление для продукта """
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    permission_classes = [IsActiveAuthenticated]
