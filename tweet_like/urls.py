from rest_framework.routers import DefaultRouter

from tweet_like.views import TweetLikeViewSet

router = DefaultRouter()
router.register(r'', TweetLikeViewSet, basename='tweetlike')
urlpatterns = router.urls