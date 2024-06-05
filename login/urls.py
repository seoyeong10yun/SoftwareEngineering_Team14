from django.urls import path
from . import views

app_name = "accounts"

urlpatterns = [
    path('login/', views.LoginView, name = 'login'),
    path('logout/', views.LogoutView, name = 'logout'),
    path('signup/', views.SignUpView, name = 'signup'),
]
