# Generated by Django 4.2.6 on 2023-10-14 10:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tweet_like', '0002_rename_user_tweetlike_owner_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tweetlike',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
