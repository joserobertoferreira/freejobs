from django.contrib.auth.models import User
from django.db import models


def avatar_upload_to(instance, filename):
    return f'avatars/{instance.user.username}/{filename}'


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone = models.CharField(max_length=20, blank=True)
    city = models.CharField(max_length=100, blank=True)
    region = models.CharField(max_length=2, blank=True)
    about = models.TextField(blank=True)
    avatar = models.ImageField(upload_to=avatar_upload_to, blank=True, null=True)
    average_rating = models.DecimalField(
        max_digits=3, decimal_places=2, default=0, editable=False
    )
    total_reviews = models.PositiveIntegerField(default=0, editable=False)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'
