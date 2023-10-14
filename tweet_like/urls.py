from django.urls import include, path
from rest_framework.routers import DefaultRouter

from tweet_like.views import TweetLikeViewSet

app_name = 'tweetlike'

router = DefaultRouter()
router.register(r'', TweetLikeViewSet, basename='tweetlike')

urlpatterns = [
    path('', include(router.urls)),
]
