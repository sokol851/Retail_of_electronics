from rest_framework import status, viewsets
from rest_framework.filters import SearchFilter
from rest_framework.response import Response

from employees.permissions import IsActiveAuthenticated
from relations.models import Partner, Product
from relations.serializers import PartnerSerializer, ProductSerializer


class PartnerViewSet(viewsets.ModelViewSet):
    serializer_class = PartnerSerializer
    queryset = Partner.objects.all()
    permission_classes = [IsActiveAuthenticated]
    filter_backends = [SearchFilter]
    search_fields = ['contact__country', 'name', 'products__name']

    def destroy(self, *args, **kwargs):
        # Получаем экземпляр партнера
        instance = self.get_object()
        # Удаляем все связанные продукты
        products = instance.products.all()
        for product in products:
            product.delete()  # Удаляем каждый продукт
        # Удаляем самого партнера
        self.perform_destroy(instance)

        # Удаляем контакт, если он не связан с другими партнёрами
        contact = instance.contact
        if not contact.partner_set.exists():
            contact.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    permission_classes = [IsActiveAuthenticated]
