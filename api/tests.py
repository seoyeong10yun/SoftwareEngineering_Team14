from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from django.contrib.auth.models import User
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
