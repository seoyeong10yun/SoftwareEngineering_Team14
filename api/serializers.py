from rest_framework import serializers

from .models import Item
from ott_recommend.models import Content
from django.contrib.auth.models import User

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ("__all__")
        #fields = ('name', 'description', 'cost')

class ContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Content
        fields = ("__all__")

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("__all__")