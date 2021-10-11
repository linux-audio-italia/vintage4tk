from rest_framework import serializers

from ..models import Brand, Recorder


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ["name"]


class RecorderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recorder
        fields = ["model", "brand"]
