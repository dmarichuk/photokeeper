from django.urls import re_path, path
from . import views

urlpatterns = [
    re_path('^$', views.view_profile, name='profile'),
    re_path('^edit/$', views.edit_profile, name='edit_profile'),
    re_path('^follow/$', views.follow_profile, name='follow_profile'),
    re_path('^unfollow/$', views.unfollow_profile, name='unfollow_profile'),

]


custom_auth_patterns = [
    path('signup/', views.SignUp.as_view(), name='sign_up'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
]

urlpatterns += custom_auth_patterns