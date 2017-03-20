from django.shortcuts import render
from picnmix.models import Album, Photo
from picnmix.forms import UserForm, AlbumForm, PhotoForm, ShareForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.shortcuts import redirect
import uuid


def get_server_side_cookie(request, cookie, default_val=None):
  val = request.session.get(cookie)
  if not val:
    val = default_val
  return val


def visitor_cookie_handler(request):
  visits = int(get_server_side_cookie(request, 'visits', '1'))
  last_visit_cookie = get_server_side_cookie(request, 'last_visit', str(datetime.now()))
  last_visit_time = datetime.strptime(last_visit_cookie[:-7], '%Y-%m-%d %H:%M:%S')

  # If it's been more than a day since the last visit...
  if (datetime.now() - last_visit_time).days > 0:
    visits = visits + 1
    # update the last visit cookie now that we have updated the count
    request.session['last_visit'] = str(datetime.now())
  else:
    visits = 1
    # set the last visit cookie
    request.session['last_visit'] = last_visit_cookie

  # Update/set the visits cookie
  request.session['visits'] = visits


def index(request):
  request.session.set_test_cookie()

  context_dict = {}

  # Obtain our Response object early so we can add cookie information.
  visitor_cookie_handler(request)
  context_dict['visits'] = request.session['visits']

  response = render(request, 'picnmix/index.html', context_dict)
  # Call function to handle the cookies

  return response


def about(request):
  if request.session.test_cookie_worked():
    print("TEST COOKIE WORKED!")
    request.session.delete_test_cookie()

  visitor_cookie_handler(request)
  context_dict = {'visits': request.session['visits']}

  response = render(request, 'picnmix/about.html', context_dict)
  return response
  # return render(request, 'picnmix/about.html', context_dict)


def show_album(request, album_name_slug):
  # Create a context dictionary which we can pass
  # to the template rendering engine.
  context_dict = {}

  try:
    # Can we find a album name slug with the given name?
    # If we can't, the .get() method raises a DoesNotExist exception.
    # So the .get() method returns one model instance or raises an exception.
    album = Album.objects.get(slug=album_name_slug)

    # Retrieve all of the associated photos.
    # Note that filter() will return a list of page objects or an empty list
    photos = Photo.objects.filter(album_id=album)

    # Adds our results list to the template context under name pages.
    context_dict['photos'] = photos

    # We also add the album object from
    # the database to the context dictionary.
    # We'll use this in the template to verify that the album exists.
    context_dict['album'] = album
  except Album.DoesNotExist:
    # We get here if we didn't find the specified album.
    # Don't do anything -
    # the template will display the "no album" message for us.
    context_dict['album'] = None
    context_dict['photos'] = None

  # Go render the response and return it to the client.
  return render(request, 'picnmix/album.html', context_dict)


def share_album(request, album_name_slug):
  context_dict = {}
  share_form = ShareForm()
  try:
    album = Album.objects.get(slug=album_name_slug)
    context_dict['album'] = album
    context_dict['share_form'] = share_form
    if request.method == 'POST':
      share_form = ShareForm(data=request.POST)
      if share_form.is_valid():
        context_dict['share_form'] = share_form
        data = album.set_share_user(share_form.cleaned_data['users'])
        context_dict['success'] = data['success']
        context_dict['error_message'] = data['error_message']
        album.save()

  except Album.DoesNotExist:
    context_dict['album'] = None
    context_dict['photos'] = None
    context_dict['success'] = False
  return render(request, 'picnmix/share_album.html', context_dict)


def add_album(request):
  form = AlbumForm()

  # A HTTP POST?
  if request.method == 'POST':
    form = AlbumForm(request.POST)

    # Have we been provided with a valid form?
    if form.is_valid():
      # Save the new album to the database.
      album = form.save(commit=False)
      album.owner_id = request.user
      album.save()
      # Now that the album is saved
      # We could give a confirmation message
      # But since the most recent category added is on the index page
      # Then we can direct the user back to the index page.
      return redirect('index')
    else:
      # The supplied form contained errors -
      # just print them to the terminal.
      print(form.errors)

  # Will handle the bad form, new form, or no form supplied cases.
  # Render the form with error messages (if any).
  return render(request, 'picnmix/add_album.html', {'form': form})


def add_photo(request, album_name_slug):
  try:
    album = Album.objects.get(slug=album_name_slug)
  except Photo.DoesNotExist:
    album = None

  form = PhotoForm()
  if request.method == 'POST':
    form = PhotoForm(request.POST, request.FILES)
    if form.is_valid():
      if album:
        photo = form.save(commit=False)
        photo.album_id = album
        photo.save()
        # if 'picture' in request.FILES:
        #   photo.image = request.FILES['picture']
        return redirect('show_album', album_name_slug)
    else:
      print(form.errors)

  context_dict = {'form': form, 'album': album}
  return render(request, 'picnmix/add_photo.html', context_dict)


def register(request):
  # A boolean value for telling the template
  # whether the registration was successful.
  # Set to False initially. Code changes value to
  # True when registration succeeds.
  registered = False

  # If it's a HTTP POST, we're interested in processing form data.
  if request.method == 'POST':
    # Attempt to grab information from the raw form information.
    # Note that we make use of both UserForm and UserProfileForm.
    user_form = UserForm(data=request.POST)

    # If the two forms are valid...
    if user_form.is_valid(): # and profile_form.is_valid():
      # Save the user's form data to the database.
      user = user_form.save()

      # Now we hash the password with the set_password method.
      # Once hashed, we can update the user object.
      user.set_password(user.password)
      user.save()

      # Now sort out the UserProfile instance.
      # Since we need to set the user attribute ourselves,
      # we set commit=False. This delays saving the model
      # until we're ready to avoid integrity problems.
      # profile = profile_form.save(commit=False)
      # profile.user = user

      # Update our variable to indicate that the template
      # registration was successful.
      registered = True
    else:
      # Invalid form or forms - mistakes or something else?
      # Print problems to the terminal.
      print(user_form.errors) # profile_form.errors)
  else:
    # Not a HTTP POST, so we render our form using two ModelForm instances.
    # These forms will be blank, ready for user input.
    user_form = UserForm()

  # Render the template depending on the context.
  return render(request,
                'picnmix/register.html',
                {'user_form': user_form,
                 'registered': registered})


def user_login(request):
  # If the request is a HTTP POST, try to pull out the relevant information.
  if request.method == 'POST':
    # Gather the username and password provided by the user.
    # This information is obtained from the login form.
    # We use request.POST.get('<variable>') as opposed
    # to request.POST['<variable>'], because the
    # request.POST.get('<variable>') returns None if the
    # value does not exist, while request.POST['<variable>']
    # will raise a KeyError exception.
    username = request.POST.get('username')
    password = request.POST.get('password')

    # Use Django's machinery to attempt to see if the username/password
    # combination is valid - a User object is returned if it is.
    user = authenticate(username=username, password=password)

    # If we have a User object, the details are correct.
    # If None (Python's way of representing the absence of a value), no user
    # with matching credentials was found.
    if user:

      # Is the account active? It could have been disabled.
      if user.is_active:
        # If the account is valid and active, we can log the user in.
        # We'll send the user back to the homepage.
        login(request, user)
        return HttpResponseRedirect(reverse('index'))
      else:
        # An inactive account was used - no logging in!
        return HttpResponse("Your account is disabled.")
    else:
      # Bad login details were provided. So we can't log the user in.
      print("Invalid login details: {0}, {1}".format(username, password))
      return render(request, 'picnmix/index.html', {})

      # The request is not a HTTP POST, so display the login form.
      # This scenario would most likely be a HTTP GET.
  else:
    # No context variables to pass to the template system, hence the
    # blank dictionary object...
    return render(request, 'picnmix/login.html', {})


def delete_album(request, album_name_slug):
  context_dict = {}
  album = Album.objects.get(slug=album_name_slug)
  context_dict['album'] = album
  if request.method == 'POST':
    if request.user.username == album.owner_id.username:
      Album.objects.filter(slug=album_name_slug).delete()
      return redirect('index')
    else:
      context_dict['success'] = False
      context_dict['message'] = 'You do not have the right to delete this album'
  return render(request, 'picnmix/delete_album.html', context_dict)

def delete_photo(request, album_name_slug, photo_id):
  context_dict = {}
  photo = Photo.objects.get(photo_id=photo_id)
  context_dict['photo'] = photo
  context_dict['album'] = photo.album_id
  if request.method == 'POST':
    if request.user.username == photo.album_id.owner_id.username:
      Photo.objects.filter(photo_id=photo.photo_id).delete()
      return redirect('show_album', album_name_slug)
    else:
      context_dict['success'] = False
      context_dict['message'] = 'You do not have the right to delete this album'
  return render(request, 'picnmix/delete_photo.html', context_dict)


@login_required
def restricted(request):
  return render(request, 'picnmix/restricted.html')


# Use the login_required() decorator to ensure only those logged in can access the view.
@login_required
def user_logout(request):
  # Since we know the user is logged in, we can now just log them out.
  logout(request)
  # Take the user back to the homepage.
  return HttpResponseRedirect(reverse('index'))