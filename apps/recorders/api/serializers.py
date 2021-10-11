from rest_framework import serializers

from ..models import Brand, Recorder


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ["id", "name", "slug", "picture", "display_name"]


class RecorderSerializer(serializers.ModelSerializer):
    brand = serializers.SlugRelatedField(many=False, read_only=True, slug_field="slug")

    class Meta:
        model = Recorder
        fields = ["id", "model", "brand", "slug", "picture", "display_name"]
