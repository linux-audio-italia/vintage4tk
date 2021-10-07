from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView
from django.views.generic.base import ContextMixin

from .models import Brand, Recorder


class BreadcrumbsMixin(ContextMixin):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["breadcrumbs"] = [("home", reverse_lazy("brand-list"))] + self.get_breadcrumbs()
        return context

    def get_breadcrumbs(self):
        return []


class BrandListView(ListView):
    context_object_name = "brands"
    model = Brand


class BrandDetailView(DetailView, BreadcrumbsMixin):
    context_object_name = "brand"
    model = Brand

    def get_breadcrumbs(self):
        current_brand = self.get_object()
        return [(current_brand.name, None)]


class RecorderDetailView(DetailView, BreadcrumbsMixin):
    context_object_name = "recorder"
    model = Recorder

    def get_queryset(self):
        return Recorder.objects.filter(
            slug=self.kwargs.get(self.slug_field), brand__slug=self.kwargs.get("brand_slug")
        )

    def get_breadcrumbs(self):
        recorder = self.get_object()
        return [
            (recorder.brand.name, reverse_lazy("brand-detail", args=[recorder.brand.slug])),
            (recorder.model, None),
        ]


class SearchResultsView(ListView, BreadcrumbsMixin):
    model = Recorder
    template_name = "recorders/search_results.html"
    context_object_name = "results"

    def get_queryset(self):
        query = self.request.GET.get("q", "")
        return Recorder.objects.filter(Q(model__icontains=query) | Q(brand__name__icontains=query))

    def get_breadcrumbs(self):
        return [("search results", None)]
