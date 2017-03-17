import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'picnmix_project.settings')
import django

django.setup()
from picnmix.models import Photo, Album, UserProfile
from django.contrib.auth.models import User
from django.utils import timezone
import glob, shutil

dirname = os.path.dirname(os.path.realpath(__file__))
pictures_path = os.path.join(dirname, 'media', 'pictures')

def populate():
  users = [
    {"name": "Alice", "password": "password", "admin": False},
    {"name": "Bob", "password": "password", "admin": False},
    {"name": "Eve", "password": "password", "admin": False},
    {"name": "admin", "password": "admin1234", "admin": True}
  ]

  albums = [
    {"name": "San Francisco", "owner": "Alice", "prefix": "san_francisco_", "shared_with": ["Bob", "Eve"]},
    {"name": "London", "owner": "Bob", "prefix": "london_", "shared_with": ["Eve"]},
    {"name": "Great Wall of China", "owner": "Eve", "prefix": "gwc_", "shared_with": ["Bob"]},
    {"name": "Skiing", "owner": "Alice", "prefix": "skiing_", "shared_with": ["Eve"]},
    {"name": "Mauritius", "owner": "Alice", "prefix": "mauritius_", "shared_with": []}
  ]

  if not os.path.isdir(pictures_path):
    os.makedirs(pictures_path)

  for user in users:
    add_user(user)

  for album in albums:
    add_album(album)


def add_album(album_dict):
  owner = User.objects.get(username=album_dict["owner"])
  shared_users = ','.join(album_dict["shared_with"])
  album = Album.objects.create(album_name=album_dict["name"], owner_id=owner, shared_users_as_string=shared_users)
  population_dir = os.path.join(dirname, "static", "population_pictures", album_dict["prefix"])
  photos = glob.glob(population_dir + "*")
  for photo in photos:
    add_photo(photo, album)
  return album


def add_photo(pic_path, album):
  (_, pic_name) = os.path.split(pic_path)
  shutil.copy2(pic_path, pictures_path)
  Photo.objects.create(album_id=album, image=os.path.join('pictures', pic_name))


def add_user(new_user):
  name = new_user["name"]
  password = new_user["password"]
  email = name + "@" + name + ".com"
  user = User.objects.create_user(name, email, password)
  user.first_name = name
  user.is_superuser = new_user["admin"]
  user.is_staff = new_user["admin"]
  user.date_joined = timezone.now()
  user.last_login = timezone.now()
  profile = UserProfile.objects.create(user=user)
  user.save()
  profile.save()

# Start execution here!
if __name__ == '__main__':
  print("Starting Picnmix population script...")
  populate()
  print "Done"
