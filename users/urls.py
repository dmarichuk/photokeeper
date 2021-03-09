from django.urls import re_path, path
from . import views

urlpatterns = [
    re_path(r'^$', views.view_profile, name='profile'),
    re_path(r'^edit/$', views.edit_profile, name='edit_profile'),
    re_path(r'^follow/$', views.handle_follow, name='follow'),
    re_path(r'^followers/$', views.followers, name='followers'),
    re_path(r'^follows/$', views.follows, name='follows'),

]


custom_auth_patterns = [
    path('signup/', views.SignUp.as_view(), name='sign_up'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
]

urlpatterns += custom_auth_patterns