from rest_framework import serializers

from .models import User, Follower


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "profile_picture")


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {'password': {'write_only': True}}


class FollowerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follower
        fields = ('follower', 'followee')

    def validate(self, attrs):
        follower = attrs.get('follower')
        followee = attrs.get('followee')

        if Follower.objects.filter(follower=follower, followee=followee).exists():
            raise serializers.ValidationError({
                'follower': ['User with this follower already exists.'],
                'followee': ['User with this followee already exists.']
            })

        return attrs
