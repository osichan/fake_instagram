from django.urls import path
from .views import UserListCreateAPIView, UserListRetrieveUpdateDestroyAPIView, FollowerListCreateView, FolloweeListView, FollowerDestroyView

urlpatterns = [
    path('users/', UserListCreateAPIView.as_view(), name='user-list'),
    path('users/<int:user_id>/', UserListRetrieveUpdateDestroyAPIView.as_view(), name='user-detail'),

    path('users/<int:follower_id>/follows/', FollowerListCreateView.as_view(), name='follower-list'),
    path('users/<int:follower_id>/follows/<int:followee_id>/', FollowerDestroyView.as_view(), name='follower-destroy'),

    path('users/<int:followee_id>/followed/', FolloweeListView.as_view(), name='followee-list'),
    path('users/<int:followee_id>/followed/<int:follower_id>/', FollowerDestroyView.as_view(), name='follower-destroy'),
]
