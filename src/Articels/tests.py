from django.test import TestCase
from .models import Article
from accounts.models import User

class ArticelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='mo', password='369')
        login = self.client.login(username='mo', password='369')
        
        self.number_of_articels = 500
        for i in range(0, self.number_of_articels):
            Article.objects.create(title="Hello World", body="hello world", author=self.user)


    def test_queryset_exists(self):
        qs = Article.objects.all()
        self.assertTrue(qs.exists())

    def test_queryset_count(self):
        qs = Article.objects.all()
        self.assertEqual(qs.count(), self.number_of_articels)