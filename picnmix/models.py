from __future__ import unicode_literals
from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
import uuid
import re


class Category(models.Model):
  name = models.CharField(max_length=128, unique=True)
  views = models.IntegerField(default=0)
  likes = models.IntegerField(default=0)
  slug = models.SlugField(unique=True)

  def save(self, *args, **kwargs):
    self.slug = slugify(self.name)
    super(Category, self).save(*args, **kwargs)

  class Meta:
    verbose_name_plural = 'Categories'

  def __str__(self):  # For Python 2, use __unicode__ too
    return self.name


class Album(models.Model):
  album_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
  album_name = models.CharField(max_length=128)
  album_description = models.CharField(max_length=256, default='')
  owner_id = models.ForeignKey(User)
  shared_users_as_string = models.CharField(max_length=2048, null=True, blank=True, default='')
  slug = models.SlugField(unique=True)
  cover_photo = models.ImageField(blank=True, null=True, default=None)

  def save(self, *args, **kwargs):
    self.slug = slugify(self.album_name)
    super(Album, self).save(*args, **kwargs)

  def set_share_user(self, share_user):
    success = True
    error_message = None

    # Remove any space from the user input
    share_user = share_user.replace(' ', '')
    # Replace multiple commas by one comma, avoiding empty string
    share_user = re.sub(',+', ',', share_user)
    # Removing duplicate entries
    user_list = list(set(share_user.split(',')))

    # Removing the owner from the shared users
    try:
      user_list.remove(self.owner_id.username)
      error_message = "You can't share an album with yourself."
    except ValueError:
      pass

    # Concatenate the two lists
    if self.shared_users_as_list() is None:
      new_user_list = user_list
    else:
      new_user_list = self.shared_users_as_list() + user_list
    # Remove duplicates
    new_user_list = list(set(new_user_list))
    new_user_list.sort()
    self.shared_users_as_string = ','.join(new_user_list)

    return {'success': success, 'error_message': error_message}

  def shared_users_as_list(self):
    if self.shared_users_as_string.split(',') != ['']:
      return self.shared_users_as_string.split(',')
    else:
      return None

  def get_cover_photo(self, photo_set):
    cover_photos = photo_set.filter(album_id=self)
    if len(cover_photos) > 0:
      self.cover_photo = cover_photos[0].image
      return cover_photos[0].image
    else:
      self.cover_photo = None
      return None

  class Meta:
    verbose_name_plural = 'Albums'

  def __str__(self):  # For Python 2, use __unicode__ too
    return self.album_name


class Photo(models.Model):
  photo_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
  album_id = models.ForeignKey(Album)
  image = models.ImageField(upload_to='media/')

  def save(self, *args, **kwargs):
    super(Photo, self).save(*args, **kwargs)

  class Meta:
    verbose_name_plural = 'Photos'

  def __str__(self):  # For Python 2, use __unicode__ too
    return str(self.photo_id)


class Page(models.Model):
  category = models.ForeignKey(Category)
  title = models.CharField(max_length=128)
  url = models.URLField()
  views = models.IntegerField(default=0)

  def __str__(self):  # For Python 2, use __unicode__ too
    return self.title


class UserProfile(models.Model):
  # This line is required. Links UserProfile to a User model instance.
  user = models.OneToOneField(User)

  # The additional attributes we wish to include.
  website = models.URLField(blank=True)
  picture = models.ImageField(upload_to='profile_images', blank=True)

  # Override the __unicode__() method to return out something meaningful!
  # Remember if you use Python 2.7.x, define __unicode__ too!
  def __str__(self):
    return self.user.username
