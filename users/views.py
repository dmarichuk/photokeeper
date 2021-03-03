from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.contrib.auth.views import LogoutView
from .forms import CreationForm, EditProfileForm
from .models import User, Follow
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from actstream import action
from actstream.actions import follow, unfollow

class SignUp(CreateView):
    form_class = CreationForm
    success_url = reverse_lazy('login')
    template_name = 'users/sign_up.html'


class CustomLogoutView(LogoutView):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.info(request, "You have successfully logged out.")
        return super().dispatch(request, *args, **kwargs)


def view_profile(request, username):
    profile = get_object_or_404(User, username=username)
    following = False
    if request.user.is_authenticated:
        if Follow.objects.filter(user=profile, follower=request.user).exists():
            following = True
    return render(
        request,
        'users/profile.html',
        {
            'profile': profile,
            'following': following,
        })


def edit_profile(request, username):
    profile = get_object_or_404(User, username=username)
    if request.user != profile:
        return redirect("profile", username=profile.username)
    form = EditProfileForm(
        request.POST or None, files=request.FILES or None, instance=profile)
    if form.is_valid():
        form.save()
        return redirect("profile", username=profile.username)
    return render(
        request,
        'users/edit_profile.html',
        {
            "profile": profile,
            "form": form,
        })


def follow(request, username):
    follower = request.user
    user = get_object_or_404(User, username=username)
    follow = Follow.objects.filter(user=user, follower=follower)
    following = follow.exists()
    if follower != user:
        if following:
            follow.delete()
            unfollow(follower, user)
            following = False
        else:
            Follow.objects.create(user=user, follower=follower)
            follow(follower, user)
            following = True
            action.send(follower, verb='started following', action_object=user)
    followers_counter = user.followers.count()
    resp = {
        'following': following,
        'followers_counter': followers_counter,
    }
    return JsonResponse(resp, safe=False)


def followers(request, username):
    profile = get_object_or_404(User, username=username)
    followers = profile.followers.all()
    return render(
        request,
        'users/followers.html',
        {
            'followers': followers,
            'profile': profile,
        }
    )


def follows(request, username):
    profile = get_object_or_404(User, username=username)
    follows = profile.follows.all()
    return render(
        request,
        'users/follows.html',
        {
            'follows': follows,
            'profile': profile,
        }
    )