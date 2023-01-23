from django.shortcuts import render, redirect
from .models import Article
from .forms import CreateArticle
from django.contrib.auth.decorators import login_required

def articel_list(request, *args, **kwargs):
    queryset = Article.objects.all().order_by('date')
    context = {
        'object_list': queryset
    }

    return render(request, 'Articels/articel_list.html', context)

def articel_detail(request, id, *args, **kwargs):
    obj = Article.objects.get(id=id)
    context = {
        'object': obj
    }
    return render(request, 'Articels/articel_detail.html', context)

@login_required(login_url='#')
def articel_create(request):
    form = CreateArticle()
    if request.method == 'POST':
        form = CreateArticle(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.author = request.user
            instance.save()
            return redirect("articles:list")
    context = {
        'form': form
    }
    return render(request, 'Articels/articel_create.html', context)

def search_view(request):
    query = request.GET.get('q')
    qs = Article.objects.search(query=query)
    context = {
        "qs": qs
    }
    return render(request, "Articels/search.html", context)