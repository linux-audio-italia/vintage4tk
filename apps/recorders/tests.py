from django.db import IntegrityError
from django.db.utils import DataError
from django.test import TestCase
from django.urls import reverse

from apps.recorders.models import Brand, Recorder


class TestCaseBrandModel(TestCase):
    def test_brand_can_be_created(self):
        yamaha = Brand.objects.create(name="yamaha")
        self.assertEqual(yamaha.name, "yamaha")
        self.assertEqual(yamaha.slug, "yamaha")

    def test_brand_slug_is_generated(self):
        hd = Brand.objects.create(name="Harman Kardon")
        self.assertEqual(hd.slug, "harman-kardon")

    def test_two_brands_cannot_be_created_with_same_name(self):
        yamaha = Brand.objects.create(name="yamaha")
        self.assertEqual(yamaha.name, "yamaha")

        with self.assertRaisesRegexp(IntegrityError, "duplicate key value violates unique constraint"):
            Brand.objects.create(name="yamaha")

    def test_brand_cannot_be_created_with_a_name_longer_than_100_characters(self):
        dummy_brand = Brand.objects.create(name="x" * 100)
        self.assertEqual(dummy_brand.name, "x" * 100)

        with self.assertRaisesRegexp(DataError, "value too long for type character varying"):
            Brand.objects.create(name="x" * 101)


class TestCaseRecorderModel(TestCase):
    fixtures = ["brands.json"]

    def test_recorder_can_be_created(self):
        yamaha = Brand.objects.get(name="yamaha")
        mt3x = Recorder.objects.create(model="mt3x", brand=yamaha)
        self.assertTrue(mt3x)

    def test_recorder_slug_is_generated(self):
        yamaha = Brand.objects.get(name="yamaha")
        mt3x = Recorder.objects.create(model="mt3x super fancy", brand=yamaha)
        self.assertEqual(mt3x.slug, "mt3x-super-fancy")

    def test_recorder_string_representation_contains_the_brand_and_the_model(self):
        yamaha = Brand.objects.get(name="yamaha")
        mt3x = Recorder.objects.create(model="mt3x", brand=yamaha)
        self.assertEqual(str(mt3x), "yamaha mt3x")

    def test_two_recorders_cannot_be_created_with_same_model_and_brand(self):
        yamaha = Brand.objects.get(name="yamaha")
        mt3x = Recorder.objects.create(model="mt3x", brand=yamaha)
        self.assertTrue(mt3x)

        with self.assertRaisesRegexp(IntegrityError, "duplicate key value violates unique constraint"):
            Recorder.objects.create(model="mt3x", brand=yamaha)

    def test_two_recorders_can_have_same_model_name_if_the_brand_is_different(self):
        yamaha = Brand.objects.get(name="yamaha")
        fostex = Brand.objects.get(name="fostex")
        dummy_recorder = Recorder.objects.create(model="dummy", brand=yamaha)
        self.assertTrue(dummy_recorder)
        dummy_recorder = Recorder.objects.create(model="dummy", brand=fostex)
        self.assertTrue(dummy_recorder)

    def test_recorder_cannot_be_created_with_a_model_longer_than_100_characters(self):
        yamaha = Brand.objects.get(name="yamaha")
        dummy_recorder = Recorder.objects.create(model="x" * 100, brand=yamaha)
        self.assertTrue(dummy_recorder)

        with self.assertRaisesRegexp(DataError, "value too long for type character varying"):
            Recorder.objects.create(model="x" * 101, brand=yamaha)


class TestCaseRecorderDetailView(TestCase):
    fixtures = ["brands.json", "recorders.json"]

    def test_recorder_detail_view_filters_by_recorder_brand(self):
        mt3x = Recorder.objects.get(brand__slug="yamaha", slug="mt3x")
        response = self.client.get(reverse("recorder-detail", kwargs={"brand_slug": "yamaha", "slug": "mt3x"}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["recorder"], mt3x)

    def test_recorder_detail_view_ignores_recorders_which_dont_have_the_right_brand(self):
        response = self.client.get(reverse("recorder-detail", kwargs={"brand_slug": "fostex", "slug": "mt3x"}))
        self.assertEqual(response.status_code, 404)
