from django.urls import path
from .views import articel_list, articel_detail, articel_create, search_view, ArticalDeleteView, ArticlUpdateView

app_name='articles'

urlpatterns = [
    path('', articel_list, name='list'),
    path('<int:id>/', articel_detail, name='detail'),
    path('create/', articel_create, name='create'),
    path("search/", search_view, name="search"),
    path("<int:pk>/delete/", ArticalDeleteView.as_view(), name="delete"),
    path("<int:pk>/update/", ArticlUpdateView.as_view(), name="update")
]