from rest_framework.routers import DefaultRouter

from relations.apps import RelationsConfig
from relations.views import PartnerViewSet, ProductViewSet

app_name = RelationsConfig.name

router = DefaultRouter()
router.register(r'partner', PartnerViewSet, basename='partner')
router.register(r'product', ProductViewSet, basename='product')

urlpatterns = [] + router.urls
