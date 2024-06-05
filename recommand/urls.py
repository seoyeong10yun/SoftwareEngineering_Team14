from django.urls import path, include
from . import views

app_name = "recommand"

urlpatterns = [
    path('content_list/', views.ContentListView, name='content_list'),
    path('content_detail/<str:content_id>/', views.ContentDetailView, name = 'content_detail'),
    path('accounts/', include('login.urls')),
]