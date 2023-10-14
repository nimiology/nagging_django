from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from users.models import MyUser


def get_user_token():
    user = MyUser.objects.create(password='1234')
    refresh = RefreshToken.for_user(user)
    return user, f'Bearer {refresh.access_token}'


class UserTest(APITestCase):
    def setUp(self) -> None:
        self.user = MyUser.objects.create_user(password='test')

    def test_get_user(self):
        response = self.client.get(reverse('users:get', kwargs={'id': self.user.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.user.pk)

    def test_get_user_not_found(self):
        response = self.client.get(reverse('users:get', kwargs={'id': self.user.pk+1}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_user_search(self):
        response = self.client.get(reverse('users:search'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class FollowingTest(APITestCase):
    def setUp(self) -> None:
        self.user1, self.token1= get_user_token()
        self.user2, self.token2 = get_user_token()
        self.client.credentials(HTTP_AUTHORIZATION=self.token2)

    def test_following(self):
        self.user2.followings.add(self.user1)
        response = self.client.get(reverse('users:followings', args=(self.user2.pk,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'][0]['id'], self.user1.pk)

    def test_followers(self):
        self.user2.followings.add(self.user1)
        response = self.client.get(reverse('users:followers', args=(self.user1.pk,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'][0]['id'], self.user2.pk)


    def test_follow_user(self):
        response = self.client.post(reverse('users:follow_user', kwargs={'id': self.user1.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.user1.pk)
        response = self.client.get(reverse('users:get', kwargs={'id': self.user1.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['following'], True)
        response = self.client.post(reverse('users:follow_user', kwargs={'id': self.user1.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['following'], False)
