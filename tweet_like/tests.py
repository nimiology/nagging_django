from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from tweet.models import Tweet
from tweet_like.models import TweetLike
from users.tests import get_user_token


class TweetLikeTest(APITestCase):
    def setUp(self) -> None:
        self.user, self.token = get_user_token()
        self.client.credentials(HTTP_AUTHORIZATION=self.token)
        self.tweet = Tweet.objects.create(owner=self.user, content='test')
        self.tweet_like = TweetLike.objects.create(tweet=self.tweet, owner=self.user)

    def test_create_tweet_like(self):
        tweet = Tweet.objects.create(owner=self.user, content='test')
        response = self.client.post(reverse('tweetlike:tweetlike-list'), data={'tweet': tweet.pk})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_tweet_like_not_authenticated(self):
        self.client.credentials()
        tweet = Tweet.objects.create(owner=self.user, content='test')
        response = self.client.post(reverse('tweetlike:tweetlike-list'), data={'tweet': tweet.pk})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_put_tweet_like(self):
        response = self.client.put(reverse('tweetlike:tweetlike-detail', args=(self.tweet_like.pk,)),
                                   data={'tweet': self.tweet.pk})
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_patch_tweet_like(self):
        response = self.client.patch(reverse('tweetlike:tweetlike-detail', args=(self.tweet_like.pk,)),
                                     data={'tweet': self.tweet.pk})
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_get_tweet_like(self):
        response = self.client.get(reverse('tweetlike:tweetlike-detail', args=(self.tweet_like.pk,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_tweet_like(self):
        response = self.client.delete(reverse('tweetlike:tweetlike-detail', args=(self.tweet_like.pk,)))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_tweet_like_not_owner(self):
        self.user, self.token = get_user_token()
        self.client.credentials(HTTP_AUTHORIZATION=self.token)
        response = self.client.delete(reverse('tweetlike:tweetlike-detail', args=(self.tweet_like.pk,)))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_tweet_like_list(self):
        response = self.client.get(reverse('tweetlike:tweetlike-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
