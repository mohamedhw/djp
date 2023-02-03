from django.urls import path
from .views import ArticelList, SearchView, Posted_by, SavedView, rm_tag, hashtag_view, saved_button, articel_detail, articel_create, ArticalDeleteView, ArticlUpdateView

app_name='articles'

urlpatterns = [
    path('', ArticelList.as_view(), name='list'),
    path('<int:id>/', articel_detail, name='detail'),
    path('create/', articel_create, name='create'),
    path('saved/', SavedView.as_view(), name="saved"),
    path("search/", SearchView.as_view(), name="search"),
    path("<int:pk>/delete/", ArticalDeleteView.as_view(), name="delete"),
    path("<int:pk>/update/", ArticlUpdateView.as_view(), name="update"),
    path("<int:pk>/save/", saved_button, name="save"),
    path("posted/<str:username>/", Posted_by.as_view(), name="posted_by"),
    path('tag/<slug:tag_slug>/', hashtag_view, name='tags'),
    path('<int:pk>/<slug:tag_slug>/', rm_tag, name="rmtag")

]