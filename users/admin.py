from django.contrib import admin

from users.models import MyUser


class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'is_staff', 'is_active')
    search_fields = list_display


admin.site.register(MyUser, UserAdmin)
