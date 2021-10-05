import os

from autoslug import AutoSlugField
from django.conf import settings
from django.contrib.staticfiles import finders
from django.db import models


class Brand(models.Model):
    name = models.CharField(max_length=100, unique=True, default="")
    slug = AutoSlugField(populate_from="name", unique=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def open_static(self, path):
        static_path = finders.find(path)
        return open(str(static_path), "rb") if static_path else None

    @property
    def picture(self):
        brand_image = self.open_static(os.path.join("brand_logos", f"{self.slug}.png"))
        fallback_image = self.open_static(settings.FALLBACK_BRAND_PICTURE)
        return brand_image or fallback_image

    class Meta:
        verbose_name_plural = "Brands"
        indexes = [models.Index(fields=["name"])]


class Recorder(models.Model):
    model = models.CharField(max_length=100)
    slug = AutoSlugField(populate_from="model", unique=False, default="")
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.brand} {self.model}"

    class Meta:
        verbose_name_plural = "Recorders"
        indexes = [models.Index(fields=["model"])]
        unique_together = ["model", "brand"]
