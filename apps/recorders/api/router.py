from rest_framework import routers

from .views import BrandViewSet, RecorderViewSet

router = routers.DefaultRouter()
router.register(r"brands", BrandViewSet)
router.register(r"recorders", RecorderViewSet)
