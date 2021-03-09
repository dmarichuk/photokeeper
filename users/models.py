from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import reverse



class User(AbstractUser):
    email = models.EmailField(_('email address'), unique=True)
    avatar = models.ImageField(
        _('profile picture'),
        help_text=_('only images formats allowed'),
        upload_to='avatars/',
        default='avatars/default/default-avatar.jpg',
        blank=True
        )

    class Meta:
        ordering = ['username']
    
    def get_absolute_url(self):
        return reverse('profile', args=[str(self.username)])
    

class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="followers"
    )

    follower = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="follows"
    )

    class Meta:
        unique_together = (
            ("user", "follower"),
        )
