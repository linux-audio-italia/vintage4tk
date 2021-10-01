from autoslug import AutoSlugField
from django.db import models


class Brand(models.Model):
    name = models.CharField(max_length=100, unique=True, default="")
    slug = AutoSlugField(populate_from="name", unique=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

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
