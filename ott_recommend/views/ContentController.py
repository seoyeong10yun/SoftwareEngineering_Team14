from django.shortcuts import render
from django.http import JsonResponse
from ..models import Content

def display(request):
    return render(request, 'display.html')

def content_info(request, slug):
    my_content = Content.objects.get(slug=slug)
    return render(request, 'contentInfo.html')

def content_list(request):
    category = request.GET.get('category', '추천')
    content = Content.objects.filter(category=category)
    data = list(content.values('title', 'description'))
    return JsonResponse(data, safe=False)