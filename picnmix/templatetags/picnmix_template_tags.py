from django import template
from picnmix.models import Category, Album, Photo

register = template.Library()

@register.inclusion_tag('picnmix/album_list.html')
def get_album_list(user=None):
  cover_photo_dict = {}
  all_albums = Album.objects.all()
  shared_albums = []
  for album in all_albums:
    shared_users = album.shared_users_as_list()

    photos = Photo.objects.filter(album_id=album)
    if len(photos) > 0:
      album.cover_photo = photos[0].image
      cover_photo_dict[album.album_name] = photos[0].image
#    cover_photo_dict[album.album_name] = cover_photo
    print album.cover_photo

    if not shared_users is None and (user.username in shared_users):
      shared_albums.append(album)

  owned_albums = all_albums.filter(owner_id=user)

  return {'owned_albums': owned_albums, 'shared_albums': shared_albums, 'cover_photo_dict': cover_photo_dict}