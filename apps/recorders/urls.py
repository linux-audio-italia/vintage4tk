from django.urls import path

from .views import BrandDetailView, BrandListView, RecorderDetailView, SearchResultsView

urlpatterns = [
    path("search/", SearchResultsView.as_view(), name="search-results"),
    path("<slug:slug>/", BrandDetailView.as_view(), name="brand-detail"),
    path("<slug:brand_slug>/<slug:slug>/", RecorderDetailView.as_view(), name="recorder-detail"),
    path("", BrandListView.as_view(), name="brand-list"),
]
