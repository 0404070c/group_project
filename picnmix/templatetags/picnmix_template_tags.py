from django import template
from picnmix.models import Album, Photo

register = template.Library()

@register.inclusion_tag('picnmix/album_list.html')
def get_album_list(user=None):
  all_albums = Album.objects.all()
  shared_albums = []
  owned_albums = []

  # Get the list of albums shared with the user and add a cover photo for every shared album
  for album in all_albums:
    # Adding a cover photo for every album
    photos = Photo.objects.filter(album_id=album)
    if len(photos) > 0:
      album.cover_photo = photos[0].image

    # Get shared user list from the album and populate the shared albums list
    shared_users = album.shared_users_as_list()
    if not shared_users is None and (user.username in shared_users):
      shared_albums.append(album)
    # Populate the owned albums list
    if album.owner_id.username == user.username:
      owned_albums.append(album)


  return {'owned_albums': owned_albums, 'shared_albums': shared_albums}