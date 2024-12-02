from django.contrib.auth import get_user_model
from django.test import TestCase

from rest_framework.test import APIClient
from .models import Profile

User = get_user_model()

class ProfileTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='cfe', password='1234')
        self.user2 = User.objects.create_user(username='cfe2', password='1234')
    
    def get_client(self):
        client = APIClient()
        client.login(username=self.user.username, password='1234')
        return client
    
    def test_profile_created(self):
        qs = Profile.objects.all()
        self.assertEqual(qs.count(), 2)
        
    def test_following(self):
        first = self.user
        second = self.user2
        first.profile.followers.add(second)
        second_user_following_whom = second.following.all()
        qs = second_user_following_whom.filter(user=first)
        first_user_following_no_one = first.following.all()
        self.assertTrue(qs.exists())
        self.assertFalse(first_user_following_no_one.exists())
        
    def test_follow_api_endpoint(self):
        client = self.get_client()
        response = client.post(
            f'/api/profiles/{self.user2.username}/follow',
            {
                "action": "follow"
            }                       
        )
        r_data = response.json()
        count = r_data.get("count")
        self.assertEqual(count, 1)
        
    def test_unfollow_api_endpoint(self):
        first = self.user
        second = self.user2
        first.profile.followers.add(second)
        client = self.get_client()
        response = client.post(
            f'/api/profiles/{self.user2.username}/follow',
            {
                "action": "unfollow"
            }                       
        )
        r_data = response.json()
        count = r_data.get("count")
        self.assertEqual(count, 0)
        
    def test_cannot_follow_api_endpoint(self):
        client = self.get_client()
        response = client.post(
            f'/api/profiles/{self.user.username}/follow',
            {
                "action": "follow"
            }                       
        )
        r_data = response.json()
        count = r_data.get("count")
        self.assertEqual(count, 0)