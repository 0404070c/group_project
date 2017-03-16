from django import forms
from django.contrib.auth.models import User
from picnmix.models import Page, Category, UserProfile, Album


class CategoryForm(forms.ModelForm):
  name = forms.CharField(max_length=128,
                         help_text="Please enter the category name.")
  views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
  likes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
  slug = forms.CharField(widget=forms.HiddenInput(), required=False)

  # An inline class to provide additional information on the form.
  class Meta:
    # Provide an association between the ModelForm and a model
    model = Category
    fields = ('name',)


class AlbumForm(forms.ModelForm):
  name = forms.CharField(max_length=128,
                         help_text="Please enter the category name.")
  slug = forms.CharField(widget=forms.HiddenInput(), required=False)

  # An inline class to provide additional information on the form.
  class Meta:
    # Provide an association between the ModelForm and a model
    model = Album
    fields = ('name',)


class PageForm(forms.ModelForm):
  title = forms.CharField(max_length=128,
                          help_text="Please enter the title of the page.")
  url = forms.URLField(max_length=200,
                       help_text="Please enter the URL of the page.")
  views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)

  def clean(self):
    cleaned_data = self.cleaned_data
    url = cleaned_data.get('url')
    # If url is not empty and doesn't start with 'http://',
    # then prepend 'http://'.
    if url and not url.startswith('http://'):
      url = 'http://' + url
      cleaned_data['url'] = url

      return cleaned_data


class PhotoForm(forms.ModelForm):
  title = forms.CharField(max_length=128,
                          help_text="Please enter the title of the page.")

  def clean(self):
    cleaned_data = self.cleaned_data
    url = cleaned_data.get('url')
    # If url is not empty and doesn't start with 'http://',
    # then prepend 'http://'.
    if url and not url.startswith('http://'):
      url = 'http://' + url
      cleaned_data['url'] = url

      return cleaned_data

  class Meta:
    # Provide an association between the ModelForm and a model
    model = Page

    # What fields do we want to include in our form?
    # This way we don't need every field in the model present.
    # Some fields may allow NULL values, so we may not want to include them.
    # Here, we are hiding the foreign key.
    # we can either exclude the category field from the form,
    exclude = ('album',)
    # or specify the fields to include (i.e. not include the category field)
    # fields = ('title', 'url', 'views')


class ShareForm(forms.ModelForm):
  users = forms.CharField(
    widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter user to share with'}))

  class Meta:
    model = Album
    fields = ('users',)


class UserForm(forms.ModelForm):
  username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
  password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))

  class Meta:
    model = User
    fields = ('username', 'password')


class UserProfileForm(forms.ModelForm):
  class Meta:
    model = UserProfile
    fields = ('website', 'picture')
