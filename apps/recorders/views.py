from .models import Brand, Recorder
from django.views.generic import DetailView, ListView


class BrandListView(ListView):
    context_object_name = "brands"
    model = Brand


class BrandDetailView(DetailView):
    context_object_name = "brand"
    model = Brand


class RecorderDetailView(DetailView):
    context_object_name = "recorder"
    model = Recorder

    def get_queryset(self):
        return Recorder.objects.filter(
            slug=self.kwargs.get(self.slug_field), brand__slug=self.kwargs.get("brand_slug")
        )
