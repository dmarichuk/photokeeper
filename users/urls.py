from django.urls import re_path, path
from . import views

urlpatterns = [
    re_path('^$', views.view_profile, name='profile'),
    re_path('^edit/$', views.edit_profile, name='edit_profile'),
    re_path('^follow/$', views.follow, name='follow'),

]


custom_auth_patterns = [
    path('signup/', views.SignUp.as_view(), name='sign_up'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
]

urlpatterns += custom_auth_patterns