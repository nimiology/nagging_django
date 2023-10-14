from django.urls import path

from users.views import UserSearch, GetUser, FollowUserAPI, FollowingAPI, FollowersAPI

app_name = 'users'
urlpatterns = [
    path('search/', UserSearch.as_view(), name='search'),
    path('get/<int:id>/', GetUser.as_view(), name='get'),

    path('follow/user/<int:id>/', FollowUserAPI.as_view(), name='follow_user'),
    path('<int:id>/following/', FollowingAPI.as_view(), name='followings'),
    path('<int:id>/follower/', FollowersAPI.as_view(), name='followers'),

]
