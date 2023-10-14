from rest_framework import serializers

from tweet.models import Tweet
from users.serializers import MyUserSerializer


class TweetSerializer(serializers.ModelSerializer):
    owner = MyUserSerializer(read_only=True)

    class Meta:
        model = Tweet
        fields = '__all__'
