from django.contrib.auth import get_user_model
from django.db import models

from tweet.models import Tweet


# Create your models here.

class TweetLike(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, editable=False)
    tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE, editable=False, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'tweet']
