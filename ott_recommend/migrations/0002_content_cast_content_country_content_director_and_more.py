# Generated by Django 5.0.6 on 2024-06-07 05:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ott_recommend', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='content',
            name='cast',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='content',
            name='country',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='content',
            name='director',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='content',
            name='duration',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='content',
            name='genre',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='content',
            name='rating',
            field=models.CharField(max_length=10),
        ),
        migrations.AlterField(
            model_name='content',
            name='title',
            field=models.CharField(max_length=200),
        ),
    ]
