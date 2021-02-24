from . import views
from django.urls import re_path

urlpatterns = [
    re_path(r'^albums/$', views.all_albums, name='all_albums'),
    re_path(r'^albums/(?P<album_id>\d+)/$', views.one_album, name='one_album'),
    re_path(r'^new_album/$', views.new_album, name='new_album'),
    re_path(r'^(?P<album_id>\d+)/edit/$', views.edit_album, name='edit_album'),
    re_path(r'^(?P<album_id>\d+)/edit/delete/$', views.delete_album, name='delete_album'),
    re_path(r'^(?P<album_id>\d+)/add_photo/$', views.add_photo, name='add_photo'),
    re_path(r'^(?P<album_id>\d+)/photos/(?P<photo_id>\d+)/$', views.get_photo, name='get_photo'),
    re_path(r'^(?P<album_id>\d+)/photos/(?P<photo_id>\d+)/edit/$', views.edit_photo, name='edit_photo'),
    re_path(r'^(?P<album_id>\d+)/photos/(?P<photo_id>\d+)/edit/delete/$', views.delete_photo, name='delete_photo'),
    re_path(r'^(?P<album_id>\d+)/photos/(?P<photo_id>\d+)/add_comment/$', views.add_comment, name='add_comment'),
    re_path(r'^(?P<album_id>\d+)/photos/(?P<photo_id>\d+)/delete_comment/(?P<comment_id>\d+)/$', views.delete_comment, name='delete_comment'),
    re_path(r'^(?P<album_id>\d+)/photos/(?P<photo_id>\d+)/add_like/$', views.add_like_view, name='add_like'),
    re_path(r'^(?P<album_id>\d+)/photos/(?P<photo_id>\d+)/delete_like/$', views.delete_like_view, name='delete_like'),
    
]
