from rest_framework import serializers
from models import User, Follower


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'name', 'username', 'password', 'bio', 'profile_picture')
        extra_kwargs = {'password': {'write_only': True}}


class FollowerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follower
        fields = ('id', 'follower_id', 'followee_id')


