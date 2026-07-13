from django.contrib import admin
from .models import Profile, MarketPrice,County, SubCounty, Ward,OfficerTask

admin.site.register(MarketPrice)
admin.site.register(OfficerTask)
@admin.register(County)
class CountyAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(SubCounty)
class SubCountyAdmin(admin.ModelAdmin):
    list_display = ("name", "county")
    search_fields = ("name",)
    list_filter = ("county",)


@admin.register(Ward)
class WardAdmin(admin.ModelAdmin):
    list_display = ("name", "sub_county")
    search_fields = ("name",)
    list_filter = ("sub_county",)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "role",
        "county",
        "sub_county",
        "ward"
    )