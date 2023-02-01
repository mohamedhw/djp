from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
from django.db.models import Q
from django.utils.text import slugify

class ArticleManager(models.Manager):

    def search(self, query=None):
        if query is None or query=="":
            return self.get_queryset().none()
        lookups = Q(title__icontains=query) | Q(body__icontains=query)
        return self.get_queryset().filter(lookups)


class Hashtag(models.Model):
    title   = models.CharField(max_length=3000, blank=True, null=True)
    tag_slug    = models.SlugField(null=False, unique=True)
    # hashtagcount    = models.IntegerField(null=True, blank=True)
    #          = models.ManyToManyField(Article)

    # atetime         = models.DateTimeField(auto_now_add=True)
    # date            = models.DateField(auto_now_add=True)
    # time            = models.TimeField(auto_now_add=True)
    # user_pk         = models.IntegerField()

    def save(self, *args, **kwargs):
        if not self.tag_slug:
            self.tag_slug = slugify(self.title)
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Article(models.Model):
    title = models.CharField(max_length=100)
    body = models.TextField()
    thumb = models.ImageField(default='default.png', blank=True, upload_to='media')
    date = models.DateTimeField(default=timezone.now())
    author = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    saved_pic = models.ManyToManyField(User, blank=True, related_name="save_pic")
    tags = models.ManyToManyField(Hashtag, related_name="tags")

    objects = ArticleManager()
    def __str__(self):
        return self.title

    def snippet(self):
        return self.body[:50] + "..."


    def get_absolute_url(self):
        return reverse("articles:detail", kwargs={"id": self.id})


