from django.db import models


class UserManager(models.Manager):
    def create_user(self, email, name, username, password, bio='', profile_picture=None):
        user = self.model(
            email=email,
            name=name,
            username=username,
            password=password,
            bio=bio,
            profile_picture=profile_picture
        )
        user.save(using=self._db)
        return user

    def update_user(self, user_id, **kwargs):
        user = self.get(pk=user_id)
        for attr, value in kwargs.items():
            setattr(user, attr, value)
        user.save(using=self._db)
        return user

    def delete_user(self, user_id):
        user = self.get(pk=user_id)
        user.delete()


class FollowerManager(models.Manager):
    def add_follower(self, follower_id, followee_id):
        follower = self.model(
            follower_id=follower_id,
            followee_id=followee_id
        )
        follower.save(using=self._db)
        return follower

    def remove_follower(self, follower_id, followee_id):
        try:
            follower = self.get(follower_id=follower_id, followee_id=followee_id)
            follower.delete()
        except self.model.DoesNotExist:
            pass


class User(models.Model):
    objects = UserManager()
    email = models.CharField(max_length=255, unique=True, null=False)
    name = models.CharField(max_length=45)
    username = models.CharField(max_length=45, unique=True, null=False)
    password = models.CharField(max_length=45, null=False)
    bio = models.CharField(max_length=255)
    profile_picture = models.IntegerField()

    def __str__(self):
        return self.username


class Follower(models.Model):
    objects = FollowerManager()
    follower_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')
    followee_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')

    def __str__(self):
        return f"{self.follower_id} -> {self.followee_id}"