# Generated by Django 3.2.9 on 2023-02-20 06:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='type',
            field=models.CharField(choices=[['f', 'Follow'], ['rl', 'Repost Like']], max_length=3),
        ),
    ]