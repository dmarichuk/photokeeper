from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from .models import Like, Tag

User = get_user_model()


def add_tag(obj, name):
    """Create tag for 'obj'."""
    obj_type = ContentType.objects.get_for_model(obj)
    tag, is_created = Tag.objects.get_or_create(
        content_type=obj_type, object_id=obj.id, name=name)
    return tag


def remove_tag(obj, name):
    """Remove tag from 'obj'."""
    obj_type = ContentType.objects.get_for_model(obj)
    Tag.objects.filter(
        content_type=obj_type, object_id=obj.id, name=name).delete()


def add_like(obj, user):
    """Like `obj`."""
    obj_type = ContentType.objects.get_for_model(obj)
    like, is_created = Like.objects.get_or_create(
        content_type=obj_type, object_id=obj.id, user=user)
    return like


def delete_like(obj, user):
    """Delete like from `obj`."""
    obj_type = ContentType.objects.get_for_model(obj)
    Like.objects.filter(
        content_type=obj_type, object_id=obj.id, user=user
    ).delete()


def is_fan(obj, user) -> bool:
    """Check if `user` likes `obj`."""
    if not user.is_authenticated:
        return False
    obj_type = ContentType.objects.get_for_model(obj)
    likes = Like.objects.filter(
        content_type=obj_type, object_id=obj.id, user=user)
    return likes.exists()


def get_fans(obj):
    """Get all users who like `obj`."""
    obj_type = ContentType.objects.get_for_model(obj)
    return User.objects.filter(
        likes__content_type=obj_type, likes__object_id=obj.id)
