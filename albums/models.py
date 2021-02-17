
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import ugettext_lazy as _

User = get_user_model()


class Album(models.Model):
    title = models.CharField(
        verbose_name=_("album's title"),
        help_text=_('50 characters allowed'),
        max_length=50)
    description = models.TextField(
        help_text=_('256 characters allowed'),
        max_length=256)
    date = models.DateTimeField(
        verbose_name=_("creation date"),
        auto_now_add=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='albums')
    tags = GenericRelation('Tag')

    class Meta:
        ordering = ['-date']

    def __unicode__(self):
        return _('%s, %s, %s') % (self.title, self.date, self.creator)


class Photo(models.Model):
    photo = models.ImageField(
        help_text=_('only images formats allowed'),
        upload_to='photos/')
    description = models.TextField(
        verbose_name=_("photo's description"),
        help_text=_('(optional field) short photo description'),
        max_length=256,
        blank=True, null=True)
    date = models.DateTimeField(
        verbose_name=_("upload date"),
        auto_now_add=True)
    creator = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='photos',
        related_query_name='photo')
    album = models.ForeignKey(
        Album,
        on_delete=models.CASCADE,
        related_name='photos',
        related_query_name='photo')
    likes = GenericRelation('Like')
    tags = GenericRelation('Tag')

    class Meta:
        ordering = ['-date']

    def __unicode__(self):
        return _("Photo's author: %s, date: %s") % (self.creator, self.date)


    @property
    def total_likes(self):
        return self.likes.count()

    @property
    def show_tags(self):
        return self.tags.all()


class Comment(models.Model):
    text = models.TextField(
        verbose_name=_('comment text'),
        max_length=512)
    date = models.DateTimeField(
        verbose_name=_("publication date"),
        auto_now_add=True)
    creator = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments')
    photo = models.ForeignKey(
        Photo,
        on_delete=models.CASCADE,
        related_name='comments')
    likes = GenericRelation('Like')

    class Meta:
        ordering = ['-date']

    def __unicode__(self):
        return _('Text: %s, Author %s') % (self.text, self.creator)

    @property
    def total_likes(self):
        return self.likes.count()


class Tag(models.Model):
    name = models.SlugField(
        verbose_name=_('tag'),
        help_text=_('32 characters allowed'),
        max_length=32)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    def __unicode__(self):
        return self.name


class Like(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='likes')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
