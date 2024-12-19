from apps import RelationsConfig
from rest_framework.routers import DefaultRouter
from views import PartnerViewSet

app_name = RelationsConfig.name

router = DefaultRouter()
router.register(r'partner', PartnerViewSet, basename='partner')

urlpatterns = [] + router.urls
