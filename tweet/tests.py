from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from tweet.models import Tweet
from tweet_like.models import TweetLike
from users.tests import get_user_token


class TweeTest(APITestCase):
    def setUp(self) -> None:
        self.user, self.token = get_user_token()
        self.client.credentials(HTTP_AUTHORIZATION=self.token)
        self.tweet = Tweet.objects.create(owner=self.user, content='test')

    def test_create_tweet(self):
        response = self.client.post(reverse('tweet:tweet-list'), data={'content': 'test'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_tweet_not_authenticated(self):
        self.client.credentials()
        response = self.client.post(reverse('tweet:tweet-list'), data={'content': 'test'})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_put_tweet(self):
        response = self.client.put(reverse('tweet:tweet-detail', args=(self.tweet.pk,)),
                                   data={'tweet': self.tweet.pk})
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_patch_tweet(self):
        response = self.client.patch(reverse('tweet:tweet-detail', args=(self.tweet.pk,)),
                                     data={'tweet': self.tweet.pk})
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_get_tweet(self):
        response = self.client.get(reverse('tweet:tweet-detail', args=(self.tweet.pk,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_tweet(self):
        response = self.client.delete(reverse('tweet:tweet-detail', args=(self.tweet.pk,)))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_tweet_not_owner(self):
        self.user, self.token = get_user_token()
        self.client.credentials(HTTP_AUTHORIZATION=self.token)
        response = self.client.delete(reverse('tweet:tweet-detail', args=(self.tweet.pk,)))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_tweet_list(self):
        response = self.client.get(reverse('tweet:tweet-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

