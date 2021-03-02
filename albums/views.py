from django.shortcuts import (
    render, get_object_or_404, get_list_or_404, redirect, )
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.views.generic.base import TemplateView, View
from .models import User, Album, Photo, Comment, Like
from .forms import AlbumForm, PhotoForm, CommentForm, EditPhotoForm
from .services import add_like, delete_like, is_fan, get_fans
from linkedlist.linked_list import CycleDoublyLinkedList as cdll
from django.db.models import Q


class IndexView(TemplateView):
    template_name = "index.html"    


def news(request):
    all_albums = Album.objects.select_related('creator').all()
    following_albums = Album.objects.filter(creator__followers__user=request.user)
    my_comments = Comment.objects.filter(photo__creator=request.user)
    
    return render(
        request,
        'index.html',
        {'all_albums': all_albums,
         'following_albums': following_albums,
         'my_comments': my_comments
         })


@login_required
def all_albums(request, username):
    creator = get_object_or_404(User, username=username)
    albums = Album.objects.filter(creator=creator)
    paginator = Paginator(albums, 8)
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
def one_album(request, username, album_id):
    album = get_object_or_404(Album, id=album_id)
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
def get_photo(request, username, album_id, photo_id):
    photos = get_list_or_404(Photo, album__id=album_id)
    lst = cdll(photos)
    album = Album.objects.get(pk=album_id)
    photo = album.photos.get(pk=photo_id)
    tags = photo.tags.all()
    liked = is_fan(photo, request.user)
    get_next = lst.get_next(photo)
    get_prev = lst.get_prev(photo)
    comments = photo.comments.all()
    paginator = Paginator(comments, 20)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(
        request,
        'albums/get_photo.html',
        {
            'photo': photo,
            'next': get_next,
            'prev': get_prev,
            'page': page,
            'paginator': paginator,
            'form': CommentForm,
            'album': album,
            'liked': liked,
            'tags': tags
        }
    )


@login_required
def new_album(request, username):
    common_tags = Album.tags.most_common()[:4]
    if request.method != 'POST':
        form = AlbumForm()
        return render(
            request,
            'albums/new_album.html',
            {
                'form': form,
                'common_tags': common_tags,
            })
    form = AlbumForm(request.POST)
    if form.is_valid():
        album = form.save(commit=False)
        album.creator = request.user
        album.save()
        form.save_m2m()
        return redirect('all_albums', username=request.user.username)
    return render(
        request,
        'albums/new_album.html',
        {
         'form': form,
         'common_tags': common_tags,
        })


@login_required
def edit_album(request, username, album_id):
    album = get_object_or_404(Album, id=album_id)
    if request.user != album.creator:
        return redirect(
            "one_album", username=album.creator, album_id=album_id)
    form = AlbumForm(
         request.POST or None, files=request.FILES or None, instance=album)
    if form.is_valid():
        form.save()
        return redirect(
            "all_albums", username=album.creator)
    return render(
        request,
        'albums/edit_album.html',
        {"album": album, "form": form}
        )


@login_required
def delete_album(request, username, album_id):
    album = get_object_or_404(Album, id=album_id)
    if request.user == album.creator:
        album.delete()
    return redirect("all_albums", username=album.creator)


@login_required
def add_photo(request, username, album_id):
    common_tags = Photo.tags.most_common()[:4]
    if request.method != "POST":
        form = PhotoForm()
        return render(
            request,
            "albums/add_photo.html",
            {
                "form": form,
                'album_id': album_id,
                'common_tags': common_tags
                })
    files = request.FILES.getlist('photo')
    for f in files:
        form = PhotoForm(request.POST, files=request.FILES)
        if form.is_valid():
            photo = form.save(commit=False)
            photo.photo = f
            photo.creator = request.user
            photo.album = Album.objects.get(pk=album_id)
            photo.save()
            form.save_m2m()
        else:
            return render(
                request,
                "albums/add_photo.html",
                {
                    "form": form,
                    'album_id': album_id,
                    'common_tags': common_tags,
                    })
    return redirect('one_album', request.user.username, album_id)


@login_required
def edit_photo(request, username, album_id, photo_id):
    album = get_object_or_404(Album, id=album_id)
    photo = album.photos.get(pk=photo_id)
    if request.user != photo.creator:
        return redirect(
            "get_photo",
            username=photo.creator,
            album_id=album_id,
            photo_id=photo_id)
    form = EditPhotoForm(
         request.POST or None, files=request.FILES or None, instance=photo)
    if form.is_valid():
        form.save()
        return redirect(
            "get_photo",
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


@login_required
def delete_photo(request, username, album_id, photo_id):
    if request.user.username == username:
        photos = get_list_or_404(Photo, album__id=album_id)
        lst = cdll(photos)
        photo = Photo.objects.get(pk=photo_id)
        get_next = lst.get_next(photo)
        photo.delete()
        return redirect(
            'get_photo',
            username=username,
            album_id=album_id,
            photo_id=get_next.id
            )
    return redirect(
        'get_photo',
        username=username,
        album_id=album_id,
        photo_id=photo_id
        )

@login_required
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
            'get_photo',
            username=username,
            album_id=album_id,
            photo_id=photo_id
        )
    return render(
        request, "albums/album_photo.html", {"photo": photo, "form": form})

@login_required
def delete_comment(request, username, album_id, photo_id, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if comment.creator == request.user:
        comment.delete()
        return redirect(
            "get_photo",
            username=username,
            album_id=album_id,
            photo_id=photo_id)
    return redirect(
            "get_photo",
            username=username,
            album_id=album_id,
            photo_id=photo_id)


@login_required
def like(request, username, photo_id):
    user = request.user
    photo = Photo.objects.get(pk=photo_id)
    liked = is_fan(photo, user)
    num_likes = len(list(get_fans(photo)))
    if liked:
        delete_like(photo, user)
    else:
        add_like(photo, user)
    resp = {
        'liked': liked,
        'num_likes': num_likes,
    }
    return JsonResponse(resp, safe=False)


def search(request):
    query = request.GET.get('q')
    users = User.objects.filter(username__icontains=query)
    photos = Photo.objects.filter(tags__name__in=[query])
    albums = Album.objects.filter(Q(title__icontains=query) | Q(tags__name__in=[query]))
    return render(
        request,
        'search.html',
        {   
            'users': users,
            'photos': photos,
            'albums': albums,
        }
    )