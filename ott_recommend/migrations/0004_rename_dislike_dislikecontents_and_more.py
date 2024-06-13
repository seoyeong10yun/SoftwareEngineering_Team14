# Generated by Django 5.0.6 on 2024-06-07 07:13

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ott_recommend', '0003_alter_favoritecontent_added_date_dislike_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Dislike',
            new_name='DislikeContents',
        ),
        migrations.RenameModel(
            old_name='Like',
            new_name='LikeContents',
        ),
        migrations.RemoveField(
            model_name='favoritecontent',
            name='content',
        ),
        migrations.RemoveField(
            model_name='favoritecontent',
            name='user',
        ),
        migrations.DeleteModel(
            name='DislikeContent',
        ),
        migrations.DeleteModel(
            name='FavoriteContent',
        ),
    ]