from django.db import IntegrityError
from django.db.utils import DataError
from django.test import TestCase
from django.urls import reverse

from apps.recorders.models import Brand, Recorder
from apps.recorders.views import BreadcrumbsMixin


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

    def test_brand_absolute_url(self):
        yamaha = Brand.objects.create(name="yamaha")
        self.assertEqual(yamaha.get_absolute_url(), "/yamaha/")


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

    def test_recorder_absolute_url(self):
        yamaha = Brand.objects.get(name="yamaha")
        mt3x = Recorder.objects.create(model="mt3x", brand=yamaha)
        self.assertEqual(mt3x.get_absolute_url(), "/yamaha/mt3x/")


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


class TestCaseBreadcrumbsMixin(TestCase):
    fixtures = ["brands.json", "recorders.json"]

    def test_breadcrumb_mixin_default_context_contains_only_the_home_link(self):
        b = BreadcrumbsMixin()
        ctx = b.get_context_data()
        self.assertEqual(ctx["breadcrumbs"], [("home", "/")])
        self.assertEqual(b.get_breadcrumbs(), [])

    def test_brand_detail_context_includes_breadcrumbs(self):
        response = self.client.get(reverse("brand-detail", args=["yamaha"]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["breadcrumbs"], [("home", "/"), ("yamaha", None)])

    def test_recorder_detail_context_includes_breadcrumbs(self):
        response = self.client.get(reverse("recorder-detail", kwargs={"brand_slug": "yamaha", "slug": "mt3x"}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["breadcrumbs"], [("home", "/"), ("yamaha", "/yamaha/"), ("mt3x", None)])


class TestCaseSidebarMixir(TestCase):
    fixtures = ["brands.json", "recorders.json"]

    def test_all_brands_are_injected_into_the_context(self):
        all_brands = Brand.objects.all()
        response = self.client.get(reverse("brand-detail", args=["yamaha"]))
        self.assertEqual(response.status_code, 200)
        self.assertTrue("sidebar" in response.context)
        self.assertTrue(list(all_brands) == list(response.context["sidebar"]["brands"]))


class TestCaseRecordersSearch(TestCase):
    fixtures = ["brands.json", "recorders.json"]

    def test_search_no_results(self):
        response = self.client.get(reverse("search-results"), {"q": "pcperi"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Sorry, no recorders match your search.")

    def test_search_with_an_empty_q_renders_everything(self):
        response = self.client.get(reverse("search-results"), {"q": ""})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(str(response.content).count('class="RecorderCard"'), 6)
        self.assertContains(response, "We found 6 recorders based on your search.")
        self.assertNotContains(response, "Sorry, no recorders match your search.")

    def test_search_without_q_parameter_renders_everything(self):
        response = self.client.get(reverse("search-results"))
        content_str = response.content.decode(response.charset)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(content_str.count('class="RecorderCard"'), 6)
        self.assertContains(response, "We found 6 recorders based on your search.")
        self.assertNotContains(response, "Sorry, no recorders match your search.")

    def test_search_in_brand_name(self):
        response = self.client.get(reverse("search-results"), {"q": "fos"})
        content_str = response.content.decode(response.charset)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(content_str.count('class="RecorderCard"'), 2)
        self.assertContains(response, "We found 2 recorders based on your search.")
        self.assertContains(response, 'href="/fostex/x-28/"')
        self.assertContains(response, 'href="/fostex/x-28h/"')
        self.assertNotContains(response, "Sorry, no recorders match your search.")

    def test_search_in_recoder_model(self):
        response = self.client.get(reverse("search-results"), {"q": "mt"})
        content_str = response.content.decode(response.charset)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(content_str.count('class="RecorderCard"'), 3)
        self.assertContains(response, "We found 3 recorders based on your search.")
        self.assertContains(response, 'href="/yamaha/mt3x/"')
        self.assertContains(response, 'href="/yamaha/mt4x/"')
        self.assertContains(response, 'href="/yamaha/mt50/"')
        self.assertNotContains(response, "Sorry, no recorders match your search.")

    def test_search_in_both_brand_name_and_recoder_model(self):
        response = self.client.get(reverse("search-results"), {"q": "h"})
        content_str = response.content.decode(response.charset)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(content_str.count('class="RecorderCard"'), 4)
        self.assertContains(response, "We found 4 recorders based on your search.")
        self.assertContains(response, 'href="/yamaha/mt3x/"')
        self.assertContains(response, 'href="/yamaha/mt4x/"')
        self.assertContains(response, 'href="/yamaha/mt50/"')
        self.assertContains(response, 'href="/fostex/x-28h/"')
        self.assertNotContains(response, 'href="/fostex/x-28/"')
        self.assertNotContains(response, "Sorry, no recorders match your search.")


class TestCaseURLS(TestCase):
    fixtures = ["brands.json", "recorders.json"]
    status_200 = ["", "/", "/yamaha/", "/yamaha/mt3x/", "/search/"]
    status_301 = ["/yamaha", "/yamaha/mt3x", "/search", "/admin"]
    status_302 = ["/admin/"]

    def test_every_url_return_an_expected_status_code(self):
        for url in self.status_200:
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200)

        for url in self.status_301:
            response = self.client.get(url)
            self.assertEqual(response.status_code, 301)

        for url in self.status_302:
            response = self.client.get(url)
            self.assertEqual(response.status_code, 302)
