from django.urls import path
from views import UserListView, UserDetailView, FollowerListView, FollowerDetailView

urlpatterns = [
    path('users/', UserListView.as_view(), name='user-list'),
    path('users/<int:user_id>/', UserDetailView.as_view(), name='user-detail'),
    path('users/<int:followee_id>/followers/', FollowerListView.as_view(), name='follower-list'),
    path('users/<int:followee_id>/followers/<int:follower_id>/', FollowerDetailView.as_view(), name='follower-detail'),
]