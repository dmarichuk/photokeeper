from . import views
from django.urls import re_path

urlpatterns = [
    re_path(r'^albums/$', views.get_all_albums, name='get_all_albums'),
    re_path(r'^albums/(?P<album_id>\d+)/$', views.get_one_album, name='get_one_album'),
    re_path(r'^new_album/$', views.create_new_album, name='create_new_album'),
    #re_path(r'^(?P<album_id>\d+)/edit/$', views.edit_one_album, name='edit_one_album'),
    re_path(r'^(?P<album_id>\d+)/add_photo/$', views.add_photo_to_album, name='add_photo_to_album'),
    re_path(r'^(?P<album_id>\d+)/photos/(?P<photo_id>\d+)/$', views.get_album_photo, name='get_album_photo'),
    re_path(r'^(?P<album_id>\d+)/photos/(?P<photo_id>\d+)/add_comment/$', views.add_comment, name='add_comment')
]
