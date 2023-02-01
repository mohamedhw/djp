from django import forms
from . import models


class CreateArticle(forms.ModelForm):
    class Meta:
        model = models.Article
        fields = ['title', 'body', 'thumb']

class HashTagForm(forms.ModelForm):
    class Meta:
        model = models.Hashtag
        fields = ['title']
