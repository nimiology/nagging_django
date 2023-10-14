from django.urls import path

from users.views import UserSearch, GetUser, FollowUserAPI, FollowingAPI, FollowersAPI, \
    GetAllTimeZonesAPI

app_name = 'users'
urlpatterns = [
    path('search/', UserSearch.as_view(), name='search'),
    path('get/<username>/', GetUser.as_view(), name='get'),

    path('follow/user/<username>/', FollowUserAPI.as_view(), name='follow_user'),
    path('<username>/following/', FollowingAPI.as_view(), name='followings'),
    path('<username>/follower/', FollowersAPI.as_view(), name='followers'),

    path('timezones/', GetAllTimeZonesAPI.as_view(), name='timezones'),

]
