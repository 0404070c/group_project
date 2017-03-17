from django import forms
from django.contrib.auth.models import User
from picnmix.models import Album, Photo


class AlbumForm(forms.ModelForm):
  album_name = forms.CharField(max_length=256, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Album name'}))

  album_description = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter a description of your new album'}), max_length=256)
  slug = forms.CharField(widget=forms.HiddenInput(), required=False)

  # An inline class to provide additional information on the form.
  class Meta:
    # Provide an association between the ModelForm and a model
    model = Album
    fields = ('album_name', 'album_description')


class PhotoForm(forms.ModelForm):
  class Meta:
    # Provide an association between the ModelForm and a model
    model = Photo

    # What fields do we want to include in our form?
    # This way we don't need every field in the model present.
    # Some fields may allow NULL values, so we may not want to include them.
    # Here, we are hiding the foreign key.
    # we can either exclude the category field from the form,
    # exclude = ('album_id',)
    # or specify the fields to include (i.e. not include the category field)
    fields = ('image',)


class ShareForm(forms.ModelForm):
  users = forms.CharField(
    widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'user1, user2, user3, etc.'}))

  class Meta:
    model = Album
    fields = ('users',)


class UserForm(forms.ModelForm):
  username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
  password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))

  class Meta:
    model = User
    fields = ('username', 'password')