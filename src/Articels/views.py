from django.shortcuts import render, redirect
from .models import Article
from .forms import CreateArticle
from django.contrib.auth.decorators import login_required
from django.views.generic import DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin


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


class ArticalDeleteView(LoginRequiredMixin, DeleteView):
    model = Article
    success_url ="/"

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

class ArticlUpdateView(LoginRequiredMixin, UpdateView):
    model = Article
    fields = ["title", "body"]
    template_name = "Articels/update.html"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

def search_view(request):
    query = request.GET.get('q')
    qs = Article.objects.search(query=query)
    print(qs)
    context = {
        "qs": qs
    }
    return render(request, "Articels/search.html", context)