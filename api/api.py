from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import *
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import authentication_classes, permission_classes
from django.utils import timezone

# 콘텐츠 리스트를 보여주는 apiview
class ContentListView(APIView):
    def get(self, request):
        model = Content.objects.all()
        serializer = ContentSerializer(model, many=True)
        return Response(serializer.data)

# 특정 콘텐츠 세부 정보를 보여주는 apiview
class ContentDetailView(APIView):
    def get(self, request, content_id):
        model = Content.objects.get(id=content_id)
        serializer = ContentSerializer(model)
        return Response(serializer.data)

# 전체 유저 리스트를 보여주는 apiview
class UserListView(APIView):
    def get(self, request):
        model = User.objects.all()
        serializer = UserSerializer(model, many=True)
        return Response(serializer.data)

# 회원가입 기능을 수행하는 apiview
@permission_classes([AllowAny])
@authentication_classes([])
class SignUpView(APIView):
    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
# 로그인 기능을 수행하는 apiview
@permission_classes([AllowAny])
@authentication_classes([])
class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 유저의 시청기록 조회를 위한 apiview
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
class WatchHistoryView(APIView):
    def get(self, request):
        user = request.user
        watch_history = WatchHistory.objects.filter(user=user)
        serializer = WatchHistorySerializer(watch_history, many=True)
        return Response(serializer.data)
    
# 사용자가 콘텐츠를 시청할 때 호출되는 api
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
class AddWatchHistoryView(APIView):
    def post(self, request):
        user = request.user
        content_id = request.data.get('content_id')
        watch_duration = request.data.get('watch_duration')

        if not content_id or not watch_duration:
            return Response({'error': 'Content ID and watch duration are required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            content = Content.objects.get(id=content_id)
        except Content.DoesNotExist:
            return Response({'error': 'Content not found'}, status=status.HTTP_404_NOT_FOUND)

        watch_history = WatchHistory.objects.create(
            user=user,
            content=content,
            watch_date=timezone.now(),
            watch_duration=watch_duration
        )

        serializer = WatchHistorySerializer(watch_history)
        return Response(serializer.data, status=status.HTTP_201_CREATED)