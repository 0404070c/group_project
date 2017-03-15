from django import template
from rango.models import Category, Album

register = template.Library()

def objectifyName(string):
    return {'name': string}

@register.inclusion_tag('rango/cats.html')
def get_category_list(cat=None):
    return {'cats': Category.objects.all(),
        'act_cat': cat}

@register.inclusion_tag('rango/album-list2.html')
def get_album_list(user=None):
    ownedAlbums = Album.objects.all().filter(ownerId=user)
    allAlbums = Album.objects.all()
    sharedAlbums = []
    for album in allAlbums:
        sharedUsers = str.split(str(album.sharedUsers), ',')
        sharedUsersObj = map(objectifyName, sharedUsers)
        print sharedUsers
        if user.username in sharedUsers:
            sharedAlbums.append(album)
        album.sharedUsersObj = sharedUsersObj

    return {'ownedAlbums': ownedAlbums, 'sharedAlbums':sharedAlbums}