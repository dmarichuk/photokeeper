from django.forms import ModelForm, MultiWidget, TextInput, SelectMultiple, ClearableFileInput
from django.utils.translation import ugettext_lazy as _
from .models import Comment, Album, Photo


class AlbumForm(ModelForm):
    class Meta:
        model = Album
        exclude = ('date', 'creator')
        labels = {
            'title': _('Title'),
            'description': _('Description'),
            'tags': _('Tags')
        }


class PhotoForm(ModelForm):
    class Meta:
        model = Photo
        fields = ('description', 'photo', 'tags')
        widgets = {
            'photo': ClearableFileInput(attrs={'multiple': True}),
        }
        labels = {
            'description': _('Description'),
            'photo': _('Photo image'),
            'tags': _('Tags')
        }


class EditPhotoForm(ModelForm):
    class Meta:
        model = Photo
        fields = ('description', 'tags')
        labels = {
            'description': _('Description'),
            'tags': _('Tags')
        }


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)
        labels = {
            'text': _('Comment\'s text'),
            }
