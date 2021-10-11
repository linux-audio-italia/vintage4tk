from autoslug import AutoSlugField
from django.db import models
from django.urls import reverse
from easy_thumbnails.fields import ThumbnailerImageField


class Brand(models.Model):
    name = models.CharField(max_length=100, unique=True, default="")
    slug = AutoSlugField(populate_from="name", unique=True, default="")
    picture = ThumbnailerImageField(
        upload_to="brands", default="brands/brand_placeholder.gif", null=False, blank=False
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("recorders:brand-detail", args=[self.slug])

    @property
    def display_name(self):
        return self.name.capitalize()

    class Meta:
        verbose_name_plural = "Brands"
        indexes = [models.Index(fields=["name"])]


class Recorder(models.Model):
    model = models.CharField(max_length=100)
    slug = AutoSlugField(populate_from="model", unique=False, default="")
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    picture = ThumbnailerImageField(
        upload_to="recorders", default="recorders/recorder_placeholder.gif", null=False, blank=False
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.brand.name} {self.model}"

    def get_absolute_url(self):
        return reverse("recorders:recorder-detail", args=[self.brand.slug, self.slug])

    @property
    def display_name(self):
        return f"{self.brand.name.capitalize()} {self.model.capitalize()}"

    class Meta:
        verbose_name_plural = "Recorders"
        indexes = [models.Index(fields=["model"])]
        unique_together = ["model", "brand"]
