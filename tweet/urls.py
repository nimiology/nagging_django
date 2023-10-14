from django.urls import include, path
from rest_framework.routers import DefaultRouter

from tweet.views import TweetModelViewSet

app_name = 'tweet'

router = DefaultRouter()
router.register(r'', TweetModelViewSet, basename='tweet')

urlpatterns = [
    path('', include(router.urls)),
]
