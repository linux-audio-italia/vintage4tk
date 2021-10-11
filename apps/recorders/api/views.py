from rest_framework import viewsets

from ..models import Brand, Recorder
from .serializers import BrandSerializer, RecorderSerializer


class BrandViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer


class RecorderViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Recorder.objects.all()
    serializer_class = RecorderSerializer
