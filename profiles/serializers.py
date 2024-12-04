from rest_framework import serializers
from .models import Profile

class PublicProfileSerializer(serializers.ModelSerializer):
    first_name = serializers.SerializerMethodField(read_only=True)
    last_name = serializers.SerializerMethodField(read_only=True)
    is_following = serializers.SerializerMethodField(read_only=True)
    username = serializers.SerializerMethodField(read_only=True)
    follower_count = serializers.SerializerMethodField(read_only=True)
    following_count = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'id', 'location', 'bio',
                  'follower_count', 'following_count', 'is_following', 'username']
        
    def get_is_following(self, obj):
        is_following = False
        context = self.context
        request = context.get('request')
        if request and request.user.is_authenticated:
            user = request.user
            followers = obj.followers.all()
            print("Current user:", user.username)
            print("Profile user:", obj.user.username)
            print("Profile followers:", [follower.username for follower in followers])
            print("Current user following:", [following.user.username for following in user.following.all()])
            is_following = user in followers
        return is_following

    def get_first_name(self, obj):
        return obj.user.first_name
    
    def get_last_name(self, obj):
        return obj.user.last_name
    
    def get_username(self, obj):
        return obj.user.username
    
    def get_following_count(self, obj):
        return obj.user.following.count()
    
    def get_follower_count(self, obj):
        return obj.followers.count()