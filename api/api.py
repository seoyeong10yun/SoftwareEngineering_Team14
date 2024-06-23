from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import *
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import authentication_classes, permission_classes
from django.utils import timezone
from django.db.models import Q, Count
import random


# 콘텐츠 리스트를 보여주는 apiview
class ContentListView(APIView):
    def get(self, request):
        paginator = PageNumberPagination()
        paginator.page_size = 10
        contents = Content.objects.all()
        result_page = paginator.paginate_queryset(contents, request)
        serializer = ContentSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

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

# 유저 로그아웃 기능을 수행하는 api 뷰
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
class LogoutView(APIView):
    def post(self, request):
        try:
            request.user.auth_token.delete()
            return Response(status=status.HTTP_200_OK)
        except (AttributeError, Token.DoesNotExist):
            return Response(status=status.HTTP_400_BAD_REQUEST)

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

        if not content_id:
            return Response({'error': 'Content ID is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            content = Content.objects.get(id=content_id)
        except Content.DoesNotExist:
            return Response({'error': 'Content not found'}, status=status.HTTP_404_NOT_FOUND)

        if WatchHistory.objects.filter(user=user, content=content).exists():
            return Response({'error': 'This content is already in your watch history'}, status=status.HTTP_400_BAD_REQUEST)

        watch_history = WatchHistory.objects.create(
            user=user,
            content=content,
            watch_date=timezone.now(),
            watch_duration=0  # Default duration
        )

        serializer = WatchHistorySerializer(watch_history)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
# 좋아요 기능을 수행하는 APIView
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
class LikeContentView(APIView):
    def post(self, request):
        user = request.user
        content_id = request.data.get('content_id')

        if not content_id:
            return Response({'error': 'Content ID is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            content = Content.objects.get(id=content_id)
        except Content.DoesNotExist:
            return Response({'error': 'Content not found'}, status=status.HTTP_404_NOT_FOUND)
        
        # Check if the content is already disliked by the user and remove it
        DislikeContent.objects.filter(user=user, content=content).delete()

        like, created = LikeContent.objects.get_or_create(user=user, content=content)
        if not created:
            return Response({'message': 'Content already liked'}, status=status.HTTP_200_OK)

        serializer = LikeContentSerializer(like)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

# 싫어요 기능을 수행하는 APIView
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
class DislikeContentView(APIView):
    def post(self, request):
        user = request.user
        content_id = request.data.get('content_id')

        if not content_id:
            return Response({'error': 'Content ID is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            content = Content.objects.get(id=content_id)
        except Content.DoesNotExist:
            return Response({'error': 'Content not found'}, status=status.HTTP_404_NOT_FOUND)
        
        # Check if the content is already liked by the user and remove it
        LikeContent.objects.filter(user=user, content=content).delete()

        dislike, created = DislikeContent.objects.get_or_create(user=user, content=content)
        if not created:
            return Response({'message': 'Content already disliked'}, status=status.HTTP_200_OK)

        serializer = DislikeContentSerializer(dislike)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
# 검색 기능을 수행하는 APIView
class ContentSearchView(APIView):
    def get(self, request):
        tag = request.query_params.get('tag')
        query = request.query_params.get('query')
        
        if not tag or not query:
            return Response({'error': 'Tag and query parameters are required'}, status=status.HTTP_400_BAD_REQUEST)
        
        filters = {
            'genre': Q(genre__icontains=query),
            'director': Q(director__icontains=query),
            'title': Q(title__icontains=query),
            'cast': Q(cast__icontains=query),
            'country': Q(country__icontains=query),
        }
        
        if tag not in filters:
            return Response({'error': 'Invalid tag'}, status=status.HTTP_400_BAD_REQUEST)
        
        contents = Content.objects.filter(filters[tag])
        serializer = ContentSerializer(contents, many=True)
        return Response(serializer.data)
    
# 추천 콘텐츠 알고리즘 APIView
class RecommendContentView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get(self, request):
        user = request.user

        # 좋아요 한 콘텐츠 가져오기
        liked_content_ids = LikeContent.objects.filter(user=user).values_list('content_id', flat=True)

        # 싫어요 한 콘텐츠 가져오기
        disliked_content_ids = DislikeContent.objects.filter(user=user).values_list('content_id', flat=True)

        # 시청 기록에서 유사한 콘텐츠 가져오기
        watch_history_content_ids = WatchHistory.objects.filter(user=user).values_list('content_id', flat=True)
        watched_contents = Content.objects.filter(id__in=watch_history_content_ids)

        recommendations = {
            'liked_genre': [],
            'liked_cast': [],
            'liked_director': [],
            'watched_genre': [],
            'watched_cast': [],
            'watched_director': []
        }

        def get_random_sample(queryset, sample_size=10):
            count = queryset.count()
            if count > sample_size:
                indices = random.sample(range(count), sample_size)
                return [queryset[i] for i in indices]
            return list(queryset)

        # 좋아요한 콘텐츠
        if liked_content_ids.exists():
            liked_genres = Content.objects.filter(id__in=liked_content_ids).values_list('genre', flat=True)
            recommendations['liked_genre'] = get_random_sample(
                Content.objects.filter(
                    genre__in=liked_genres
                ).exclude(id__in=disliked_content_ids).distinct()
            )

            liked_casts = Content.objects.filter(id__in=liked_content_ids).values_list('cast', flat=True)
            cast_list = []
            for cast in liked_casts:
                cast_list.extend(cast.split(','))

            cast_query = Q()
            for cast in cast_list:
                cast_query |= Q(cast__icontains=cast.strip())

            recommendations['liked_cast'] = get_random_sample(
                Content.objects.filter(
                    cast_query
                ).exclude(id__in=disliked_content_ids).distinct()
            )

            liked_directors = Content.objects.filter(id__in=liked_content_ids).values_list('director', flat=True)
            recommendations['liked_director'] = get_random_sample(
                Content.objects.filter(
                    director__in=liked_directors
                ).exclude(id__in=disliked_content_ids).distinct()
            )

        # 시청한 콘텐츠
        if watch_history_content_ids.exists():
            watched_genres = watched_contents.values_list('genre', flat=True)
            recommendations['watched_genre'] = get_random_sample(
                Content.objects.filter(
                    genre__in=watched_genres
                ).exclude(id__in=disliked_content_ids).distinct()
            )

            watched_casts = watched_contents.values_list('cast', flat=True)
            cast_list = []
            for cast in watched_casts:
                cast_list.extend(cast.split(','))

            cast_query = Q()
            for cast in cast_list:
                cast_query |= Q(cast__icontains=cast.strip())

            recommendations['watched_cast'] = get_random_sample(
                Content.objects.filter(
                    cast_query
                ).exclude(id__in=disliked_content_ids).distinct()
            )

            watched_directors = watched_contents.values_list('director', flat=True)
            recommendations['watched_director'] = get_random_sample(
                Content.objects.filter(
                    director__in=watched_directors
                ).exclude(id__in=disliked_content_ids).distinct()
            )

        response_data = {
            'liked_genre': ContentSerializer(recommendations['liked_genre'], many=True).data,
            'liked_cast': ContentSerializer(recommendations['liked_cast'], many=True).data,
            'liked_director': ContentSerializer(recommendations['liked_director'], many=True).data,
            'watched_genre': ContentSerializer(recommendations['watched_genre'], many=True).data,
            'watched_cast': ContentSerializer(recommendations['watched_cast'], many=True).data,
            'watched_director': ContentSerializer(recommendations['watched_director'], many=True).data,
            'liked_content_exists': liked_content_ids.exists(),
            'watch_history_exists': watch_history_content_ids.exists()
        }

        return Response(response_data, status=status.HTTP_200_OK)
        
# 장르별 컨텐츠를 출력하는 APIView
class GenreContentView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get(self, request, genre):
        paginator = PageNumberPagination()
        paginator.page_size = 10  # 페이지당 10개의 항목을 표시
        contents = Content.objects.filter(genre__icontains=genre)
        result_page = paginator.paginate_queryset(contents, request)
        serializer = ContentSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)