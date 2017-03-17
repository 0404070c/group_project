from django.contrib import admin
from picnmix.models import UserProfile, Album, Photo

class AlbumAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('album_name',)}

admin.site.register(UserProfile)
admin.site.register(Album, AlbumAdmin)
admin.site.register(Photo)