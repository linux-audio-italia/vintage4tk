from django.test import TestCase

from ..models import Brand, Recorder
from .serializers import BrandSerializer, RecorderSerializer


class TestCaseBrandSerializer(TestCase):
    def test_brand_can_be_serialized(self):
        yamaha = Brand.objects.create(name="yamaha")
        got = BrandSerializer(yamaha)
        expected = {
            "id": yamaha.id,
            "name": yamaha.name,
            "slug": yamaha.slug,
            "picture": yamaha.picture.url,
            "display_name": yamaha.display_name,
        }
        self.assertEqual(got.data, expected)

    def test_brand_can_be_deserialized(self):
        expected = BrandSerializer(
            data={
                "name": "yamaha",
                "display_name": "Yamaha",
                "slug": "yamaha",
            }
        )
        self.assertTrue(expected.is_valid())


class TestCaseRecorderSerializer(TestCase):
    fixtures = ["brands.json"]

    def test_recorder_can_be_serialized(self):
        yamaha = Brand.objects.get(name="yamaha")
        mt3x = Recorder.objects.create(model="mt3x", brand=yamaha)
        got = RecorderSerializer(mt3x)
        expected = {
            "id": mt3x.id,
            "model": mt3x.model,
            "brand": mt3x.brand.slug,
            "slug": mt3x.slug,
            "picture": mt3x.picture.url,
            "display_name": mt3x.display_name,
        }
        self.assertEqual(got.data, expected)
