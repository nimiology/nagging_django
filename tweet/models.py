from django.contrib.auth import get_user_model
from django.db import models


# Create your models here.
class Tweet(models.Model):
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    reply = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)
    content = models.CharField(max_length=221)
    created_at = models.DateTimeField(auto_now_add=True)
