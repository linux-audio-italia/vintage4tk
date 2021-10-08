import typing

from django.conf import settings
from django.contrib import admin
from django.contrib.sitemaps import GenericSitemap
from django.contrib.sitemaps.views import sitemap
from django.urls import URLPattern, URLResolver, include, path, re_path
from django.views.static import serve

from apps.recorders.models import Brand, Recorder

URL = typing.Union[URLPattern, URLResolver]
URLList = typing.List[URL]


def sitemap_info(model, order_field):
    return {"queryset": model.objects.order_by(order_field), "date_field": "updated_at"}


SITEMAPS = {
    "brands": GenericSitemap(sitemap_info(Brand, "name"), priority=0.5),
    "recorders": GenericSitemap(sitemap_info(Recorder, "model"), priority=0.9),
}

urlpatterns: URLList = [
    path("admin/", admin.site.urls),
    path("", include("apps.recorders.urls")),
    path("sitemap.xml", sitemap, {"sitemaps": SITEMAPS}, name="django.contrib.sitemaps.views.sitemap"),
]

if settings.DEBUG:
    urlpatterns += [
        re_path(
            r"^media/(?P<path>.*)$",
            serve,
            {
                "document_root": settings.MEDIA_ROOT,
            },
        ),
    ]
