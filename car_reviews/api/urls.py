from rest_framework.routers import DefaultRouter
from .views import CountryViewSet, ManufacturerViewSet, CarViewSet, CommentViewSet

router = DefaultRouter()
router.register(r'countries', CountryViewSet)
router.register(r'manufacturers', ManufacturerViewSet)
router.register(r'cars', CarViewSet)
router.register(r'comments', CommentViewSet)

urlpatterns = router.urls
