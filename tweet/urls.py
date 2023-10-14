from rest_framework.routers import DefaultRouter

from tweet.views import TweetModelViewSet

router = DefaultRouter()
router.register(r'', TweetModelViewSet, basename='tweet')
urlpatterns = router.urls