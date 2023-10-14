from django.contrib.auth import get_user_model

from art.sitemaps import MySitemap


class MyUserSitemap(MySitemap):
    changefreq = 'daily'
    priority = 0.3

    def items(self):
        return get_user_model().objects.all()

    def location(self, item):
        return f'/users/{item.username}'
