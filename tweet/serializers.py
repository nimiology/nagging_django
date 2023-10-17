from rest_framework import serializers

from tweet.models import Tweet
from tweet_like.models import TweetLike
from users.serializers import FollowingUserSerializer


class TweetSerializer(serializers.ModelSerializer):
    owner = FollowingUserSerializer(read_only=True)
    user_like = serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField()

    class Meta:
        model = Tweet
        fields = '__all__'

    def _user(self):
        request = self.context.get('request', None)
        if request:
            return request.user
        return None

    def get_user_like(self, obj):
        user = self._user()
        if user is not None:
            if user.is_authenticated:
                try:
                    return TweetLike.objects.get(owner=user, tweet=obj).pk
                except TweetLike.DoesNotExist:
                    pass
        return None

    def get_likes_count(self, obj):
        return obj.likes.count()
