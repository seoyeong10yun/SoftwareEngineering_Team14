from django.shortcuts import render, get_object_or_404
from .models import ContentInfo

# Create your views here.
def ContentListView(request):
    contents = ContentInfo.objects.all()
    context = {
        'contents' : contents,
    }
    return render(request, 'recommand/content_list.html', context=context)

def ContentDetailView(request, content_id):
    content = get_object_or_404(ContentInfo, content_id=content_id)
    context = {
        'content' : content,
    }
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(request, 'recommand/content_detail_ajax.html', context=context)
    else:
        return render(request, 'recommand/content_detail.html', context=context)
    