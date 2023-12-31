# Generated by Django 4.2.6 on 2023-10-14 10:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tweet', '0004_alter_tweet_owner'),
        ('tweet_like', '0003_alter_tweetlike_owner'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tweetlike',
            name='tweet',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='likes', to='tweet.tweet'),
        ),
    ]
