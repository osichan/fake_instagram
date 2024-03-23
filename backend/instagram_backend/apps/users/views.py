from rest_framework import generics
from models import User, Follower
from serializers import UserSerializer, FollowerSerializer


class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_queryset(self):
        return User.objects.values('username', 'profile_picture')


class UserDetailView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class FollowerListView(generics.ListAPIView):
    serializer_class = UserSerializer

    def get_queryset(self):
        followee_id = self.kwargs.get('followee_id')
        return Follower.objects.filter(followee_id=followee_id)



class FollowerDetailView(generics.RetrieveAPIView):
    queryset = Follower.objects.all()
    serializer_class = FollowerSerializer