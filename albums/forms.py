from django.forms import ModelForm, MultiWidget, TextInput, SelectMultiple,ClearableFileInput
from django.utils.translation import ugettext_lazy as _
from .models import Comment, Album, Photo


class AlbumForm(ModelForm):
    class Meta:
        model = Album
        exclude = ('date', 'creator')
        widgets = {
            'tags': MultiWidget(widgets=[TextInput, SelectMultiple])
        }
        labels = {
            'title': _('Title'),
            'description': _('Description'),
            'tags': _('Tags (optional)')
        }


class PhotoForm(ModelForm):
    class Meta:
        model = Photo
        fields = ('description', 'photo',)
        widgets = {
            'tags': MultiWidget(widgets=[TextInput, SelectMultiple]),
            'photo': ClearableFileInput(attrs={'multiple': True}),
        }
        labels = {
            'description': _('Description'),
            'photo': _('Photo image'),
            'tags': _('Tags (optional)')
        }


class EditPhotoForm(ModelForm):
    class Meta:
        model = Photo
        fields = ('description',)
        labels = {
            'description': _('Description'),
            'tags': _('Tags (optional)')
        }


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)
        labels = {
            'text': _('Comment\'s text'),
            }
