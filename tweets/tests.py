from django.contrib.auth import get_user_model
from django.test import TestCase

from rest_framework.test import APIClient

from .models import Tweet
# Create your tests here.

User = get_user_model()

class TweetTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='cfe', password='1234')
        self.user2 = User.objects.create_user(username='cfe2', password='1234')
        Tweet.objects.create(user=self.user, content='first tweet')
        Tweet.objects.create(user=self.user, content='third tweet')
        Tweet.objects.create(user=self.user, content='fourth tweet')
        Tweet.objects.create(user=self.user2, content='user 2 first tweet')
        self.current_count = Tweet.objects.all().count()
        
    def test_tweet_created(self):
        tweet_obj = Tweet.objects.create(user=self.user, content='second tweet')
        self.assertTrue(tweet_obj.id, 4)
        self.assertTrue(tweet_obj.user, self.user)
        
    def get_client(self):
        client = APIClient()
        client.login(username=self.user.username, password='1234')
        return client

    def test_tweet_list(self):
        client = self.get_client()
        response = client.get('/api/tweets/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 4)
        
    def test_action_like(self):
        client = self.get_client()
        response = client.post('/api/tweets/action/', {'id': 1, 'action': 'like'})
        self.assertEqual(response.status_code, 200)
        likes = response.json().get('likes')
        self.assertEqual(likes, 1)
        
    def test_action_unlike(self):
        client = self.get_client()
        response = client.post('/api/tweets/action/', {'id': 2, 'action': 'like'})
        self.assertEqual(response.status_code, 200)
        response = client.post('/api/tweets/action/', {'id': 2, 'action': 'unlike'})
        self.assertEqual(response.status_code, 200)
        likes = response.json().get('likes')
        self.assertEqual(likes, 0)
        
    def test_action_retweet(self):
        client = self.get_client()
        current_count = self.current_count
        response = client.post('/api/tweets/action/', {'id': 2, 'action': 'retweet'})
        self.assertEqual(response.status_code, 201)
        data = response.json()
        new_tweet_id = data.get('id')
        self.assertNotEqual(new_tweet_id, 2)
        self.assertEqual(current_count + 1, new_tweet_id)
        
    def test_tweet_create_api_view(self):
        request_data = {
            'content': 'new tweet'
        }
        client = self.get_client()
        response = client.post('/api/tweets/create/', request_data)
        self.assertEqual(response.status_code, 201)
        response_data = response.json()
        new_tweet_id = response_data.get('id')
        self.assertEqual(self.current_count + 1, new_tweet_id)
        
    def test_tweet_detail_api_view(self):
        client = self.get_client()
        response = client.get('/api/tweets/3/')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        _id = data.get('id')
        self.assertEqual(_id, 3)
        
    def test_tweet_delete_api_view(self):
        client = self.get_client()
        response = client.delete('/api/tweets/3/delete/')
        self.assertEqual(response.status_code, 200)
        client = self.get_client()
        response = client.delete('/api/tweets/3/delete/')
        self.assertEqual(response.status_code, 404)
        
        response_incorrect_user = client.get('/api/tweets/4/delete/')
        self.assertEqual(response_incorrect_user.status_code, 405)