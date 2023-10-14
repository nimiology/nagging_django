from django.contrib.auth.models import AbstractUser
from django.db import models
import pytz
from django.urls import reverse

from django.contrib.auth.models import BaseUserManager


class CustomUserManager(BaseUserManager):
    def create_user(self, password, **extra_fields):
        user = self.model(**extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, **extra_fields):
        user = self.create_user(**extra_fields)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class MyUser(AbstractUser):
    username = None
    email = None
    first_name = None
    last_name = None

    USERNAME_FIELD = 'id'
    REQUIRED_FIELDS = []

    id = models.AutoField(primary_key=True)
    followings = models.ManyToManyField('self', blank=True, related_name='followers', symmetrical=False, )
    bio = models.TextField(max_length=500, blank=True)
    link = models.URLField(max_length=200, blank=True)
    location = models.CharField(max_length=50, blank=True)

    objects = CustomUserManager()

    def followings_count(self) -> int:
        return self.followings.count()

    def followers_count(self):
        return self.followers.count()

    def get_absolute_url(self):
        return reverse('users:get', kwargs={'username': self.username})

    class Meta(AbstractUser.Meta):
        swappable = 'AUTH_USER_MODEL'
