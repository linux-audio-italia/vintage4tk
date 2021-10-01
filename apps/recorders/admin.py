from django.contrib import admin

from apps.recorders.models import Brand, Recorder


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ("name",)
    list_filter = ("name",)
    search_fields = ("name",)


@admin.register(Recorder)
class RecorderAdmin(admin.ModelAdmin):
    list_display = ("model", "brand")
    list_filter = ("model", "brand")
    search_fields = ("model", "brand")
