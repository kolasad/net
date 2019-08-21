from django.contrib import admin

from tracking.models import TrackingInfo


@admin.register(TrackingInfo)
class TrackingInfoAdmin(admin.ModelAdmin):
    pass
