# from django.core.cache import cache
from rest_framework import serializers
from users.models import MyUser


class MyUserSerializer(serializers.ModelSerializer):
    following = serializers.SerializerMethodField()

    class Meta:
        model = MyUser
        fields = [
            'id',
            'date_joined',
            'bio',
            'link',
            'location',
            'following',
            'followings_count',
            'followers_count',
        ]

    def _user(self):
        request = self.context.get('request', None)
        if request is not None:
            return request.user
        return None

    def get_following(self, obj):
        user = self._user()
        if user is not None:
            if user.is_authenticated:
                if obj in user.followings.all():
                    return True
        return False


class FollowingUserSerializer(MyUserSerializer):
    class Meta:
        model = MyUser
        fields = [
            'id',
            'following',
        ]
        read_only_fields = fields

    def to_representation(self, instance):
        return super(serializers.ModelSerializer, self).to_representation(instance)



