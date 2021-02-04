from django.contrib import admin
from .models import Album, Photo, Comment


class AlbumAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'description', 'date', 'creator')


class PhotoAdmin(admin.ModelAdmin):
    list_display = ('photo', 'description', 'date', 'creator', 'album',)
    search_fields = ('tag',)


admin.site.register(Album, AlbumAdmin)
admin.site.register(Photo, PhotoAdmin)
