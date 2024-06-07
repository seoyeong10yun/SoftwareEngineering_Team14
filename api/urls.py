from django.urls import include, path
from rest_framework import routers
from . import views #views.py import

router = routers.DefaultRouter() #DefaultRouter를 설정
router.register('Item', views.ItemViewSet) #itemviewset 과 item이라는 router 등록

urlpatterns = [
    path('', include(router.urls))
]