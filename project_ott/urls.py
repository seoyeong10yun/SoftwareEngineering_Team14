from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView, RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('', RedirectView.as_view(url='/login/', permanent=False)),
    path('login/', TemplateView.as_view(template_name='myapp/login.html'), name='login'),
    path('register/', TemplateView.as_view(template_name='myapp/registration.html'), name='register'),
    path('home/', TemplateView.as_view(template_name='myapp/home.html'), name='home'),
    path('content/<int:content_id>/', TemplateView.as_view(template_name='myapp/contentInfo.html'), name='content-info'),
]
