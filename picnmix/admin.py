from django.contrib import admin
from rango.models import Category, Page
from rango.models import UserProfile, Album, Photo


class PageAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'url')

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}

class AlbumAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('album_name',)}

admin.site.register(Category, CategoryAdmin)
admin.site.register(Page, PageAdmin)
admin.site.register(UserProfile)

admin.site.register(Album, AlbumAdmin)
admin.site.register(Photo)
