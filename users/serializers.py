# from django.core.cache import cache
from rest_framework import serializers
from users.models import MyUser


class MyUserSerializer(serializers.ModelSerializer):
    following = serializers.SerializerMethodField()

    class Meta:
        model = MyUser
        fields = [
            'id',
            'first_name',
            'username',
            'profile_img',
            'header_img',
            'date_joined',
            'bio',
            'link',
            'location',
            'artist',
            'verify',
            'following',
            'followings_count',
            'followers_count',
            'artist_followings_count',
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

    def to_representation(self, instance):
        data = super(MyUserSerializer, self).to_representation(instance)

        user = self.context.get('request').user
        if user == instance:
            data['last_name'] = instance.last_name
            data['email'] = instance.email
            data['timezone'] = instance.timezone
            data['setting'] = instance.setting

        return data


class FollowingUserSerializer(MyUserSerializer):
    class Meta:
        model = MyUser
        fields = [
            'id',
            'username',
            'first_name',
            'profile_img',
            'following',
            'verify',
            'artist',
        ]
        read_only_fields = fields

    def to_representation(self, instance):
        return super(serializers.ModelSerializer, self).to_representation(instance)



