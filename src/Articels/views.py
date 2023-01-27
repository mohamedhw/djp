from django.shortcuts import render, redirect
from .models import Article
from .forms import CreateArticle
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

@login_required
def saved_view(request):
    user = request.user
    pics = user.save_pic.all()
    context={
        "pics": pics,
    }
    return render(request, "Articels/saved_pic.html", context)

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