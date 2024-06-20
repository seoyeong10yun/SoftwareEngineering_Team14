from rest_framework import serializers

from .models import Item
from ott_recommend.models import Content, WatchHistory, LikeContent, DislikeContent
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ("__all__")
        #fields = ('name', 'description', 'cost')

# 콘텐츠 정보 조회용
class ContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Content
        fields = ("__all__")

# 유저 정보 조회용
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("__all__")

# 새로운 유저 회원가입용
class SignUpSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'password1','password2')

    def validate(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError("Passwords do not match")
        return data
    
    def create(self, validated_data):
        validated_data.pop('password2') # password2 필드는 User 모델에 저장하지 않는다.
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password1'],
        )
        return user

# 유저 로그인용
class LoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)

    class Meta:
        model = User
        fields = ('username', 'password')

    def validate(self, data):
        user = authenticate(username=data['username'], password=data['password'])
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Invaild credentials")
    
#시청 기록 조회용
class WatchHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = WatchHistory
        fields = '__all__'

#좋아요한 컨텐츠
class LikeContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = LikeContent
        fields = '__all__'

#싫어요한 컨텐츠
class DislikeContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = DislikeContent
        fields = '__all__'