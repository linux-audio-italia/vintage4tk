from django.urls import path
from .views import RecorderDetailView, BrandDetailView, BrandListView

urlpatterns = [
    path("", BrandListView.as_view(), name="brand-list"),
    path("<slug:slug>", BrandDetailView.as_view(), name="brand-detail"),
    path("<slug:brand_slug>/<slug:slug>", RecorderDetailView.as_view(), name="recorder-detail"),
]
