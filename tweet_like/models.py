from django.contrib.auth import get_user_model
from django.db import models

from tweet.models import Tweet


# Create your models here.

class TweetLike(models.Model):
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['owner', 'tweet']
