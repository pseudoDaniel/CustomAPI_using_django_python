from rest_framework import serializers
from . import models 

#Serializers help in transforming json strings to python objects and Vice versa 

class HelloSerializer(serializers.Serializer):
    """Serializes a name field for testing our APIView"""
    name = serializers.CharField(max_length=10)
    
class UserProfileSerializer(serializers.ModelSerializer):
    """A Serializer for our user profile objects"""
    class Meta:
        model = models.UserProfile
        #Use the profile model
        fields = ('id','email','name','password')
        #find extra keyword arguments for our model
        #we dont want people to see the password
        #so we define the extra-key word args
        #in English i mean take the fields id,email ,name and password
        #and make the password unseen while typing
        extra_kwargs = {'password':{'write_only':True}}
    def create(self, validated_data):
        """Create and return a new user."""
        user = models.UserProfile(
            email=validated_data['email'],
            name=validated_data['name']
        )
        
        return user
class ProfileFeedItemSerializer(serializers.ModelSerializer):
    """A serializer for profile feed items."""
    class Meta:
        model = models.ProfileFeedItem
        fields = ('id','user_profile','status_text','created_on')
        extra_kwargs = {'user_profile':{'read_only':True}}