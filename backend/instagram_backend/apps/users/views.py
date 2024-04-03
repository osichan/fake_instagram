from rest_framework import generics, status
from rest_framework.response import Response

from .models import User, Follower
from .serializers import UserListSerializer, UserDetailSerializer, FollowerSerializer
from django.shortcuts import get_object_or_404


class UserListCreateAPIView(generics.ListCreateAPIView):
    queryset = User.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return UserDetailSerializer
        return UserListSerializer


class UserListRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserDetailSerializer

    def get_object(self):
        user_id = self.kwargs.get('user_id')
        return get_object_or_404(User, id=user_id)

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"message": "User deleted successfully."}, status=status.HTTP_204_NO_CONTENT)


class FolloweeListView(generics.ListAPIView):
    serializer_class = FollowerSerializer

    def get_queryset(self):
        user_id = self.kwargs.get('followee_id')
        user = get_object_or_404(User, id=user_id)
        follower_ids = Follower.objects.filter(followee=user).values_list('follower', flat=True)
        followers = User.objects.filter(id__in=follower_ids)
        return followers

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = UserListSerializer(queryset, many=True)
        return Response(serializer.data)


class FollowerListCreateView(generics.ListCreateAPIView):
    serializer_class = FollowerSerializer

    def get_queryset(self):
        user_id = self.kwargs.get('follower_id')
        user = get_object_or_404(User, id=user_id)
        followee_ids = Follower.objects.filter(follower=user).values_list('followee', flat=True)
        followers = User.objects.filter(id__in=followee_ids)
        return followers

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = UserListSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        followee_id = request.data.get('followee')
        follower_id = kwargs.get('follower_id')

        if followee_id == follower_id:
            return Response({'message': 'Followee and follower cannot be the same.'},
                            status=status.HTTP_400_BAD_REQUEST)

        if Follower.objects.filter(followee=followee_id, follower=follower_id).exists():
            return Response({'message': 'Already follows.'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data={**request.data, 'follower': follower_id})

        if serializer.is_valid():
            follower = Follower.objects.add_follower(**serializer.validated_data)
            return Response(FollowerSerializer(follower).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FollowerDestroyView(generics.DestroyAPIView):
    serializer_class = FollowerSerializer

    def destroy(self, request, *args, **kwargs):
        get_object_or_404(Follower, followee=kwargs.get('followee_id'), follower=kwargs.get('follower_id'))
        Follower.objects.remove_follower(kwargs.get('followee_id'), kwargs.get('follower_id'))
        return Response({'message': 'Follower deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)
