from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import *
from rest_framework import status

# 콘텐츠 리스트를 보여주는 apiview
class ContentList(APIView):
    def get(self, request):
        model = Content.objects.all()
        serializer = ContentSerializer(model, many=True)
        return Response(serializer.data)

# 특정 콘텐츠 세부 정보를 보여주는 apiview
class ContentDetail(APIView):
    def get(self, request, content_id):
        model = Content.objects.get(id=content_id)
        serializer = ContentSerializer(model)
        return Response(serializer.data)

# 전체 유저 리스트를 보여주는 apiview
class UserList(APIView):
    def get(self, request):
        model = User.objects.all()
        serializer = UserSerializer(model, many=True)
        return Response(serializer.data)

# 회원가입 기능을 수행하는 apiview
class SignUpView(APIView):
    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)