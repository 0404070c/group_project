from django.conf.urls import url
from picnmix import views

urlpatterns = [
  url(r'^$', views.index, name='index'),
  url(r'^about', views.about, name='about'),
  url(r'^add_album/$', views.add_album, name='add_album'),
  url(r'^album/(?P<album_name_slug>[\w\-]+)/add_photo/$',
      views.add_photo,
      name='add_photo'),
  url(r'^album/(?P<album_name_slug>[\w\-]+)/share_album/$',
      views.share_album,
      name='share_album'),
  url(r'^album/(?P<album_name_slug>[\w\-]+)/$',
      views.show_album,
      name='show_album'),
  url(r'^register/$',
      views.register,
      name='register'),
  url(r'^login/$', views.user_login, name='login'),
  url(r'^restricted/', views.restricted, name='restricted'),
  url(r'^logout/$', views.user_logout, name='logout'),
]
