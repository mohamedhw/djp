from django.shortcuts import render, redirect, get_object_or_404
from .models import Article, Hashtag
from django.contrib.auth.models import User
from .forms import CreateArticle, HashTagForm
from django.contrib.auth.decorators import login_required
from django.views.generic import DeleteView, UpdateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
# from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http.response import JsonResponse




class ArticelList(ListView):
    model= Article
    template_name="Articels/articel_list.html"
    paginate_by=9

# def articel_list(request, *args, **kwargs):
#     queryset = Article.objects.all().order_by('date')
#     context = {
#         'object_list': queryset
#     }

#     return render(request, 'Articels/articel_list.html', context)

def articel_detail(request, id, *args, **kwargs):
    obj = Article.objects.get(id=id)
    # tags = Hashtag.objects.filter(article_pk=obj)
    context = {
        'object': obj,
        # 'tags': tags
    }
    return render(request, 'Articels/articel_detail.html', context)


@login_required(login_url='#')
def articel_create(request):
    form = CreateArticle()
    form_h = HashTagForm()

    if request.method == 'POST':
        form_h = HashTagForm(request.POST)
        form = CreateArticle(request.POST, request.FILES)
        if form.is_valid() and form_h.is_valid():
            insatnce_h = form_h.save()
            insatnce_h.save()
            instance = form.save(commit=False)
            instance.author = request.user
            instance.save()
            instance.tags.add(insatnce_h.id)
            instance.save()
            print(instance.id)
            
            return redirect("articles:detail", instance.pk)

    context = {
        'form': form,
        'form_h': form_h
    }
    return render(request, 'Articels/articel_create.html', context)


# @login_required
# def hashtag_create(request):
#     form = HashTagForm()
#     if request.method == 'POST':
#         form = HashTagForm(request.POST)
#         if form.is_valid():
#             instance = form.save(commit=False)
#             instance.

class ArticalDeleteView(LoginRequiredMixin, DeleteView):
    model = Article
    success_url ="/"

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

def hash_update_view(request):
    
    pass

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

# def search_view(request):
#     query = request.GET.get('q')
#     qs = Article.objects.search(query=query)

#     # paginate
#     page = request.GET.get('page', 1)
#     qs_paginator = Paginator(qs, PIC_BY_PAGE)
#     print("the qs_paginator ====", qs_paginator)
#     try:
#         qs=qs_paginator.page(page)
#     except EmptyPage:
#         qs=qs_paginator.page(qs_paginator.num_pages)
#     except PageNotAnInteger:
#         qs=qs_paginator.page(PIC_BY_PAGE)
#     print(qs)

#     context = {
#         "qs": qs,
#     }
#     return render(request, "Articels/search.html", context)

# class FilterList(ListView):
#     filterset_class=None
#     def get_queryset(self, *args, **kwargs):
#         query = self.request.GET.get('q')
#         qs1 = Article.objects.search(query=query)
#         self.filterset_class=qs1
#         print(self.filterset_class)
#         return self.filterset_class

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         # Pass the filterset to the template - it provides the form.
#         context['filterset'] = self.filterset_class
#         return context

class SavedView(ListView):
    model = Article
    template_name= "Articels/saved_pic.html"
    context_object_name="pics"
    paginate_by= 3

    def get_queryset(self):
        user = self.request.user
        return user.save_pic.all()
# @login_required
# def saved_view(request):

#     context={
#         "pics": pics,
#     }
#     return render(request, "Articels/saved_pic.html", context)

@login_required
def saved_button(request, pk):
    if request.POST.get('action') == 'post':
        data = {}
        pics = Article.objects.get(pk=pk)
        if request.user in pics.saved_pic.all():
            pics.saved_pic.remove(request.user)
        else:
            pics.saved_pic.add(request.user)
            
    return JsonResponse({"data": data})

class Posted_by(ListView):
    model=Article
    template_name = "Articels/posted_by.html"
    context_object_name= "pics"
    paginate_by=9

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Article.objects.filter(author=user).order_by('-date') 

class SearchView(ListView):
    model= Article
    template_name="Articels/search.html"
    paginate_by=6
    
    def get_queryset(self, *args, **kwargs):
        query = self.request.GET.get('q')
        qs = Article.objects.search(query=query)
        self.filterset_class=qs
        print(self.filterset_class)
        return self.filterset_class


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get('q')
        # Pass the filterset to the template - it provides the form.
        # context['object_list'] = qs
        context['query']=query
        return context
    # def get(self, request, *args, **kwargs):
    #     query = self.request.GET.get('q')
    #     qs = Article.objects.search(query=query)
    #     context={"qs": qs}
    #     return render(request, "Articels/search.html", context)


def hashtag_view(request, tag_slug):
    tag = get_object_or_404(Hashtag, tag_slug=tag_slug)
    articles = Article.objects.filter(tags=tag)
    context = {
        'articles': articles,
        'tag': tag
    }
    return render(request, "Articels/filter_tag.html", context)