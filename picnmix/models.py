from __future__ import unicode_literals
from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
import uuid
import re

# THE ALBUM MODEL, WITH A UNIQUE ID, AND EACH TIED TO AN OWNER, AND MULTIPLE SHARED USERS
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

    # REMOVE ANY SPACE FROM THE USER INPUT
    share_user = share_user.replace(' ', '')
    # REPLACE MULTIPLE COMMAS BY ONE COMMA, AVOIDING EMPTY STRING
    share_user = re.sub(',+', ',', share_user)
    # REMOVING DUPLICATE ENTRIES
    user_list = list(set(share_user.split(',')))

    # REMOVING THE OWNER FROM THE LIST OF SHARED USERS
    try:
      user_list.remove(self.owner_id.username)
      error_message = "You can't share an album with yourself."
    except ValueError:
      pass

    # CONCATENATE THE TWO LISTS
    if self.shared_users_as_list() is None:
      new_user_list = user_list
    else:
      new_user_list = self.shared_users_as_list() + user_list
    # REMOVE DUPLICATES
    new_user_list = list(set(new_user_list))
    new_user_list.sort()
    self.shared_users_as_string = ','.join(new_user_list)

    return {'success': success, 'error_message': error_message}

  def shared_users_as_list(self):
    if self.shared_users_as_string.split(',') != ['']:
      return self.shared_users_as_string.split(',')
    else:
      return None

  class Meta:
    verbose_name_plural = 'Albums'

  def __str__(self):  # For Python 2, use __unicode__ too
    return self.album_name

# THE PHOTO MODEL, WITH EACH PHOTO TIED TO AN ALBUM, AND EACH HAVING A UNIQUE ID
class Photo(models.Model):
  photo_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
  album_id = models.ForeignKey(Album)
  image = models.ImageField(upload_to='pictures/')

  def save(self, *args, **kwargs):
    super(Photo, self).save(*args, **kwargs)

  class Meta:
    verbose_name_plural = 'Photos'

  def __str__(self):  # For Python 2, use __unicode__ too
    return str(self.photo_id)

# USERPROFILE, EXTENDING THE USER MODEL
class UserProfile(models.Model):
  # This line is required. Links UserProfile to a User model instance.
  user = models.OneToOneField(User)

  # Override the __unicode__() method to return out something meaningful!
  # Remember if you use Python 2.7.x, define __unicode__ too!
  def __str__(self):
    return self.user.username