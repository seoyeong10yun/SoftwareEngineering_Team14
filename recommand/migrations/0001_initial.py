# Generated by Django 5.0.6 on 2024-06-05 04:57

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ContentInfo',
            fields=[
                ('content_id', models.CharField(max_length=255, primary_key=True, serialize=False, unique=True)),
                ('title', models.CharField(max_length=255)),
                ('director', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('genre', models.CharField(max_length=255)),
            ],
        ),
    ]
