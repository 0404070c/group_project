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
    albumId = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    albumName = models.CharField(max_length=128)
    albumDesc = models.CharField(max_length=256, default='')
    ownerId = models.ForeignKey(User)
    sharedUsers = models.CharField(max_length=2048, null=True, blank=True, default='')
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.albumName)
        super(Album, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Albums'

    def __str__(self):  # For Python 2, use __unicode__ too
        return self.albumName


class Photo(models.Model):
    photoID = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    albumId = models.ForeignKey(Album)
    image = models.ImageField(upload_to='media/')

    def save(self, *args, **kwargs):
        super(Photo, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Photos'

    def __str__(self):  # For Python 2, use __unicode__ too
        return str(self.photoID)

    def __repr__(self):  # For Python 2, use __unicode__ too
        return repr(self)



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
