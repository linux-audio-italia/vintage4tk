from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView

from .models import Brand, Recorder


class BrandListView(ListView):
    context_object_name = "brands"
    model = Brand


class BrandDetailView(DetailView):
    context_object_name = "brand"
    model = Brand

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_brand = self.get_object()
        context["breadcrumbs"] = [("home", reverse_lazy("brand-list")), (current_brand.name, None)]
        return context


class RecorderDetailView(DetailView):
    context_object_name = "recorder"
    model = Recorder

    def get_queryset(self):
        return Recorder.objects.filter(
            slug=self.kwargs.get(self.slug_field), brand__slug=self.kwargs.get("brand_slug")
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        recorder = self.get_object()
        context["breadcrumbs"] = [
            ("home", reverse_lazy("brand-list")),
            (recorder.brand.name, reverse_lazy("brand-detail", args=[recorder.brand.slug])),
            (recorder.model, None),
        ]
        return context
