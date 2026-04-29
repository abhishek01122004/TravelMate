from django.contrib import admin

from .models import Attraction, Destination


@admin.register(Destination)
class DestinationAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "best_time")
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name", "slug")


@admin.register(Attraction)
class AttractionAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "destination",
        "category",
        "estimated_time",
        "priority",
        "approx_cost",
    )
    list_filter = ("destination", "category")
