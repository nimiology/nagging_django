from rest_framework import serializers

from users.serializers import MyUserSerializer
from .models import TweetLike


class TweetLikeSerializer(serializers.ModelSerializer):
    owner = MyUserSerializer(read_only=True)

    class Meta:
        model = TweetLike
        fields = '__all__'
