from django.contrib.auth.models import AbstractUser
from django.db import models
import pytz
from django.urls import reverse

from config import settings
from users.utils import user_profile_upload_file


class MyUser(AbstractUser):
    followings = models.ManyToManyField('self', blank=True, related_name='followers', symmetrical=False, )
    following_artists = models.ManyToManyField('artist.Artist', blank=True, related_name='followers')
    profile_img = models.ImageField(upload_to=user_profile_upload_file, default='profile.jpg')
    header_img = models.ImageField(upload_to=user_profile_upload_file, default='header.jpg')
    bio = models.TextField(max_length=500, blank=True)
    link = models.URLField(max_length=200, blank=True)
    location = models.CharField(max_length=50, blank=True)
    timezone = models.CharField(max_length=3,
                                choices=[(str(number), pytz.all_timezones[number]) for number in
                                         range(0, len(pytz.all_timezones))],
                                default=str(pytz.all_timezones.index(settings.TIME_ZONE)))
    setting = models.JSONField(null=True, blank=True)
    verify = models.BooleanField(default=False)

    def followings_count(self) -> int:
        return self.followings.count()

    def followers_count(self):
        return self.followers.count()

    def artist_followings_count(self) -> int:
        return self.following_artists.count()

    def get_absolute_url(self):
        return reverse('users:get', kwargs={'username': self.username})

    class Meta(AbstractUser.Meta):
        swappable = 'AUTH_USER_MODEL'


