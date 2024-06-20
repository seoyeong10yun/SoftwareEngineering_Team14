from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from django.contrib.auth.models import User
from ott_recommend.models import Content, WatchHistory, LikeContent, DislikeContent
from django.utils import timezone
# Create your tests here.

class SignUpTestCase(TestCase):
    # 테스트 전 초기화
    def setUp(self):
        self.client = APIClient()

    # 회원가입 테스트 진행
    def test_signup(self):
        url = reverse('signup')
        data = {
            "username" : "testuser",
            "password1" : "testpassword",
            "password2" : "testpassword"
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # 회원가입이 되어 DB에 들어갔는지 확인
        user_exists = User.objects.filter(username='testuser').exists()
        self.assertTrue(user_exists)

    # 테스트 종료 후 데이터 정리
    # 테스트 도중 생성된 데이터는 테스트가 종료되면 자동으로 롤백된다.
    # 즉 테스트가 완료되면 해당 유저는 DB에서 자동으로 삭제됨.
    def testDown(self):
        pass

class LoginTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.login_url = reverse('login')
        # 임의의 유저 생성
        self.user = User.objects.create_user(
            username='logintestuser',
            password='logintestpassword',
        )

    def test_user_login(self):
        login_data = {
            'username' : 'logintestuser',
            'password' : 'logintestpassword',
        }
        response = self.client.post(self.login_url, login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)

    def tets_login_wrong_password(self):
        login_data = {
            'username' : 'logintestuser',
            'password' : 'wrongpassword',
        }
        response = self.client.post(self.login_url, login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('token', response.data)

    def test_login_nonexist_user(self):
        login_data = {
            'username' : 'nonexistuser',
            'password' : 'testpassword',
        }
        response = self.client.post(self.login_url, login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('token', response.data)

#시청기록조회 테스트
class WatchHistoryAPITest(TestCase):
    def setUp(self):
        # 유저 생성
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client = APIClient()
        
        # 유저 인증 후 토큰 획득
        response = self.client.post('/api/login/', {'username': 'testuser', 'password': 'testpassword'}, format='json')
        self.token = response.data['token']
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)

        # 임시 테스트 콘텐츠 생성
        self.content1 = Content.objects.create(
            title='Test Content 1',
            genre='Drama',
            release_date='2023-01-01',
            rating='PG',
            description='Test Description 1'
        )
        self.content2 = Content.objects.create(
            title='Test Content 2',
            genre='Comedy',
            release_date='2023-01-02',
            rating='PG-13',
            description='Test Description 2'
        )

    def test_add_watch_history(self):
        response1 = self.client.post('/api/add_watch_history/', {
            'content_id': self.content1.id,
            'watch_duration': 120
        }, format='json')
        self.assertEqual(response1.status_code, 201)
        self.assertEqual(response1.data['content'], self.content1.id)
        self.assertEqual(response1.data['watch_duration'], 120)
        
        response2 = self.client.post('/api/add_watch_history/', {
            'content_id': self.content2.id,
            'watch_duration': 90
        }, format='json')
        self.assertEqual(response2.status_code, 201)
        self.assertEqual(response2.data['content'], self.content2.id)
        self.assertEqual(response2.data['watch_duration'], 90)

    def test_watch_history_list(self):
        response = self.client.get('/api/watch_history/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 0)

        self.client.post('/api/add_watch_history/', {
            'content_id': self.content1.id,
            'watch_duration': 120
        }, format='json')
        self.client.post('/api/add_watch_history/', {
            'content_id': self.content2.id,
            'watch_duration': 90
        }, format='json')

        response = self.client.get('/api/watch_history/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['content'], self.content1.id)
        self.assertEqual(response.data[1]['content'], self.content2.id)

    def tearDown(self):
        # 임시로 만들어준 테스트 항목들 삭제
        WatchHistory.objects.filter(user=self.user).delete()
        self.content1.delete()
        self.content2.delete()
        self.user.delete()

#좋아요/싫어요 테스트
class ContentInteractionAPITest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client = APIClient()

        response = self.client.post('/api/login/', {'username': 'testuser', 'password': 'testpassword'}, format='json')
        self.token = response.data['token']
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)

        self.content1 = Content.objects.create(
            title='Test Content 1',
            genre='Drama',
            release_date='2023-01-01',
            rating='PG',
            description='Test Description 1'
        )
        self.content2 = Content.objects.create(
            title='Test Content 2',
            genre='Comedy',
            release_date='2023-01-02',
            rating='PG-13',
            description='Test Description 2'
        )

    def test_like_content(self):
        response = self.client.post('/api/like_content/', {'content_id': self.content1.id}, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['content'], self.content1.id)
        self.assertEqual(response.data['user'], self.user.id)

        response = self.client.post('/api/like_content/', {'content_id': self.content1.id}, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['message'], 'Content already liked')

    def test_dislike_content(self):
        response = self.client.post('/api/dislike_content/', {'content_id': self.content2.id}, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['content'], self.content2.id)
        self.assertEqual(response.data['user'], self.user.id)

        response = self.client.post('/api/dislike_content/', {'content_id': self.content2.id}, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['message'], 'Content already disliked')

    def tearDown(self):
        LikeContent.objects.filter(user=self.user).delete()
        DislikeContent.objects.filter(user=self.user).delete()
        self.content1.delete()
        self.content2.delete()
        self.user.delete()