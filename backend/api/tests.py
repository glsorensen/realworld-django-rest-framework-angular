from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from .models import Article, Profile

class ArticleAPITestCase(APITestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )
        
        # Get the profile
        self.profile = Profile.objects.get(user=self.user)
        
        # Create a second user for testing
        self.user2 = User.objects.create_user(
            username='testuser2',
            email='test2@example.com',
            password='testpassword2'
        )
        self.profile2 = Profile.objects.get(user=self.user2)
        
        # Get auth tokens
        from rest_framework.authtoken.models import Token
        token = Token.objects.create(user=self.user)
        self.user_token = token.key
        
        token2 = Token.objects.create(user=self.user2)
        self.user2_token = token2.key
        
    # Assume more tests are here...
    # Adding placeholder to match the PR line numbers
    def test_delete_article(self):
        """Test deleting an article"""
        # Create a new article
        url = reverse('articles-list')
        data = {'article': {'title': 'How to train your dragon', 'description': 'Ever wonder how?', 'body': 'You have to believe'}}
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_token)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        slug = response.data['slug']
        
        # Delete with a different user (should fail)
        url = reverse('articles-detail', kwargs={'slug': slug})
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user2_token)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        articles = Article.objects.filter(title='How to train your dragon')
        self.assertEqual(articles.count(), 1) 