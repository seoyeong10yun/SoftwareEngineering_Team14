from django.shortcuts import render
from ..models import Movie

def display(request):
    movies = Movie.objects.all()
    return render(request, 'display.html', {'movies': movies})

def content_info(request, slug):
    movie = Movie.objects.get(slug=slug)
    return render(request, 'contentInfo.html', {'movie': movie})
