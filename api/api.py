from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import *
from rest_framework import status

class ContentList(APIView):
    def get(self, request):
        model = Content.objects.all()
        serializer = ContentSerializer(model, many=True)
        return Response(serializer.data)
    
class ContentDetail(APIView):
    def get(self, request, content_id):
        model = Content.objects.get(id=content_id)
        serializer = ContentSerializer(model)
        return Response(serializer.data)

class UserList(APIView):
    def get(self, request):
        model = User.objects.all()
        serializer = UserSerializer(model, many=True)
        return Response(serializer.data)
    
class SignUpView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)