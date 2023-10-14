from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from art.models import Artist
from notification.models import Notification
from users.models import MyUser


def get_user_token(username):
    user = MyUser.objects.create(username=username, password='1234')
    refresh = RefreshToken.for_user(user)
    return user, f'Bearer {refresh.access_token}'


class UserTest(APITestCase):
    def setUp(self) -> None:
        self.user = MyUser.objects.create_user(username='John', first_name='John', last_name='Doe',
                                               email='test@test.com', password='test')

    def test_get_user(self):
        response = self.client.get(reverse('users:get', kwargs={'username': 'John'}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'John')

    def test_get_user_not_found(self):
        response = self.client.get(reverse('users:get', kwargs={'username': 'John2'}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_user_search(self):
        response = self.client.get(reverse('users:search'), {'first_name': 'John'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'][0]['first_name'], 'John')


class FollowingTest(APITestCase):
    def setUp(self) -> None:
        self.user1, self.token1= get_user_token('Jane')
        self.user2, self.token2 = get_user_token('John')
        self.artist = Artist.objects.create(name='asdf')
        self.client.credentials(HTTP_AUTHORIZATION=self.token2)

    def test_following(self):
        self.user2.followings.add(self.user1)
        response = self.client.get(reverse('users:followings', args=(self.user2.username,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'][0]['username'], self.user1.username)

    def test_following_artists(self):
        self.user1.following_artists.add(self.artist)
        response = self.client.get(reverse('users:following_artists', args=(self.user1.username,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'][0]['id'], self.artist.pk)

    def test_followers(self):
        self.user2.followings.add(self.user1)
        response = self.client.get(reverse('users:followers', args=(self.user1.username,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'][0]['username'], self.user2.username)

    def test_follow_artist(self):
        response = self.client.post(reverse('users:follow_artist', kwargs={'pk': self.artist.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.artist.pk)
        response = self.client.get(reverse('artist:artist-detail', kwargs={'pk': self.artist.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['following'], True)
        response = self.client.post(reverse('users:follow_artist', kwargs={'pk': self.artist.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['following'], False)

    def test_follow_user(self):
        response = self.client.post(reverse('users:follow_user', kwargs={'username': self.user1.username}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], self.user1.username)
        response = self.client.get(reverse('users:get', kwargs={'username': self.user1.username}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['following'], True)
        response = self.client.post(reverse('users:follow_user', kwargs={'username': self.user1.username}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['following'], False)

    def test_get_notifications(self):
        response = self.client.get(reverse('notification:notification'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_mark_as_read(self):
        response = self.client.post(reverse('users:follow_user', kwargs={'username': self.user1.username}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.post(reverse('users:follow_user', kwargs={'username': self.user1.username}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.post(reverse('users:follow_user', kwargs={'username': self.user1.username}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        notifications = Notification.objects.all()
        for notification in notifications:
            self.assertEqual(notification.is_read, False)

        self.client.credentials(HTTP_AUTHORIZATION=self.token1)
        self.client.post(reverse('notification:markasread', args=(notifications.last().pk,)))
        response = self.client.post(reverse('notification:notification'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'][0]['obj']['username'], self.user2.username)

        notifications = Notification.objects.all()
        self.assertEqual(notifications[0].is_read, True)
        self.assertEqual(notifications[1].is_read, True)
        for notification in notifications:
            self.assertEqual(notification.is_read, True)


class GetAllTimeZonesTest(APITestCase):
    def test_all_time_zones_get(self):
        response = self.client.get(reverse('users:timezones'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
