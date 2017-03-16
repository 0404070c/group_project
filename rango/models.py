from __future__ import unicode_literals
from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
import uuid


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

  def shared_users_as_list(self):
    if self.shared_users_as_string.split(',') != ['']:
      return self.shared_users_as_string.split(',')
    else:
      return None

  def get_cover_photo(self, photo_set):
    cover_photos = photo_set.filter(album_id=self, is_cover_photo=True)
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
  is_cover_photo = models.BooleanField(default=False)

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
