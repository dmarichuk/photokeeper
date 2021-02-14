from django.shortcuts import (
    render, get_object_or_404, get_list_or_404, redirect)
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.views.generic.base import TemplateView
from .models import User, Album, Photo
from .forms import AlbumForm, PhotoForm, CommentForm
from linkedlist.linked_list import CycleDoublyLinkedList as cdll


class IndexView(TemplateView):
    template_name = "index.html"


@login_required
def get_all_albums(request, username):
    albums = Album.objects.filter(creator__username=username)
    creator = User.objects.get(username=username)
    paginator = Paginator(albums, 9)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(
        request,
        'albums/all_albums.html',
        {'page': page,
         'paginator': paginator,
         'creator': creator
         })


@login_required
def get_one_album(request, username, album_id):
    album = Album.objects.get(pk=album_id)
    photos = album.photos.all()
    paginator = Paginator(photos, 20)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(
        request,
        'albums/one_album.html',
        {'page': page,
         'paginator': paginator,
         'album': album
         })


@login_required
def get_album_photo(request, username, album_id, photo_id):
    photos = get_list_or_404(Photo, album__id=album_id)
    lst = cdll(photos)
    photo = Photo.objects.get(pk=photo_id)
    get_next = lst.get_next(photo)
    get_prev = lst.get_prev(photo)
    comments = photo.comments.all()
    paginator = Paginator(comments, 20)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(
        request,
        'albums/album_photo.html',
        {
            'photo': photo,
            'next': get_next,
            'prev': get_prev,
            'page': page,
            'paginator': paginator,
            'form': CommentForm,
            'album_id': album_id
        }
    )


@login_required
def create_new_album(request, username):
    if request.method != "POST":
        form = AlbumForm()
        return render(request, "albums/create_new_album.html", {"form": form})
    form = AlbumForm(request.POST)
    if form.is_valid():
        album = form.save(commit=False)
        album.creator = request.user
        album.save()
        return redirect('get_all_albums', request.user.username)
    return render(request, 'albums/create_new_album.html', {"form": form})


def edit_album(request, username, album_id):
    album = get_object_or_404(Album, creator__username=username, id=album_id)
    if request.user != album.creator:
        return redirect(
            "get_one_album", username=album.creator, album_id=album_id)
    form = AlbumForm(
         request.POST or None, files=request.FILES or None, instance=album)
    if form.is_valid():
        form.save()
        return redirect(
            "get_all_albums", username=album.creator)
    return render(
        request,
        'albums/edit_album.html',
        {"album": album, "form": form}
        )


def delete_album(request, username, album_id):
    album = Album.objects.get(pk=album_id)
    if request.user == album.creator:
        album.delete()
    return redirect("get_all_albums", username=album.creator)


@login_required()
def add_photo_to_album(request, username, album_id):
    if request.method != "POST":
        form = PhotoForm()
        return render(
            request,
            "albums/add_photo_to_album.html",
            {"form": form, 'album_id': album_id})
    files = request.FILES.getlist('photo')
    for f in files:
        form = PhotoForm(request.POST, files=request.FILES)
        if form.is_valid():
            photo = form.save(commit=False)
            photo.photo = f
            photo.creator = request.user
            photo.album = Album.objects.get(pk=album_id)
            photo.save()
        else:
            return render(
                request,
                "albums/add_photo_to_album.html",
                {"form": form, 'album_id': album_id})
    return redirect('get_one_album', request.user.username, album_id)


def edit_photo(request, username, album_id, photo_id):
    album = Album.objects.get(pk=album_id)
    photo = album.photos.get(pk=photo_id)
    if request.user != photo.creator:
        return redirect(
            "get_album_photo",
            username=photo.creator,
            album_id=album_id,
            photo_id=photo_id)
    form = PhotoForm(
         request.POST or None, files=request.FILES or None, instance=photo)
    if form.is_valid():
        form.save()
        return redirect(
            "get_album_photo",
            username=photo.creator,
            album_id=album_id,
            photo_id=photo_id)
    return render(
        request,
        'albums/edit_photo.html',
        {
            "album": album,
            "photo": photo,
            "form": form
        })


def delete_photo(request, username, album_id, photo_id):
    photo = get_object_or_404(pk=photo_id)
    photo.delete()
    return redirect('get_one_album', username=username, album_id=album_id)


@login_required()
def add_comment(request, username, album_id, photo_id):
    photo = get_object_or_404(
        Photo,
        album__id=album_id,
        id=photo_id)
    if request.method != "POST":
        form = CommentForm()
        return render(
            request, "albums/album_photo.html", {"photo": photo, "form": form})
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.creator = request.user
        comment.photo = photo
        comment.save()
        return redirect(
            'get_album_photo',
            username=username,
            album_id=album_id,
            photo_id=photo_id
        )
    return render(
        request, "albums/album_photo.html", {"photo": photo, "form": form})


def delete_comment(request):
    pass


def add_like(request):
    pass


def delete_like(request):
    pass
