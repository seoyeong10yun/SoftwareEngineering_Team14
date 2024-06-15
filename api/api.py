from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import *
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import authentication_classes, permission_classes

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