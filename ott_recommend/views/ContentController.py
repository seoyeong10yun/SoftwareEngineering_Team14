from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from ..models import Content

def display(request):
    return render(request, 'display.html')

def content_info(request, slug):
    my_content = get_object_or_404(Content, slug=slug)
    return render(request, 'contentInfo.html', {'my_content': my_content})

def content_list(request):
    category = request.GET.get('category', '추천')
    content = Content.objects.filter(category=category)
    data = list(content.values('title', 'description'))
    return JsonResponse(data, safe=False)
