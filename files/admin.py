from django.contrib import admin

from files.models import FileHolder, UrlHolder


@admin.register(FileHolder)
class FileHolderAdmin(admin.ModelAdmin):
    pass


@admin.register(UrlHolder)
class UrlHolderAdmin(admin.ModelAdmin):
    pass
