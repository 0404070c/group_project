from django import template
from picnmix.models import Category, Album, Photo

register = template.Library()

@register.inclusion_tag('picnmix/album_list.html')
def get_album_list(user=None):
  all_albums = Album.objects.all()
  shared_albums = []

  # Get the list of albums shared with the user and add a cover photo for every shared album
  for album in all_albums:
    shared_users = album.shared_users_as_list()
    if not shared_users is None and (user.username in shared_users):
      photos = Photo.objects.filter(album_id=album)
      if len(photos) > 0:
        album.cover_photo = photos[0].image
      shared_albums.append(album)

  # Get the list of albums owned by the user
  owned_albums = all_albums.filter(owner_id=user)
  # Add a cover photo for every owned album
  for album in owned_albums:
    photos = Photo.objects.filter(album_id=album)
    if len(photos) > 0:
      album.cover_photo = photos[0].image

  return {'owned_albums': owned_albums, 'shared_albums': shared_albums}