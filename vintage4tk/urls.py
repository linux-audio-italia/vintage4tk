import typing

from django.conf import settings
from django.contrib import admin
from django.urls import URLPattern, URLResolver, include, path, re_path
from django.views.static import serve

URL = typing.Union[URLPattern, URLResolver]
URLList = typing.List[URL]

urlpatterns: URLList = [
    path("", include("apps.recorders.urls")),
    path("admin/", admin.site.urls),
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
