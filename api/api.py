from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import *

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