from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
from django.db.models import Q


class ArticleManager(models.Manager):

    def search(self, query=None):
        if query is None or query=="":
            return self.get_queryset().none()
        lookups = Q(title__icontains=query) | Q(body__icontains=query)
        return self.get_queryset().filter(lookups)


class Article(models.Model):
    title = models.CharField(max_length=100)
    body = models.TextField()
    thumb = models.ImageField(default='default.png', blank=True, upload_to='media')
    date = models.DateTimeField(default=timezone.now())
    author = models.ForeignKey(User, on_delete=models.CASCADE, default=None)


    objects = ArticleManager()
    def __str__(self):
        return self.title

    def snippet(self):
        return self.body[:50] + "..."


    def get_absolute_url(self):
        return reverse("articles:detail", kwargs={"id": self.id})    