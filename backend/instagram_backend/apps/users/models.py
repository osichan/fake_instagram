from django.db import models


class UserManager(models.Manager):
    def create_user(self, email: str, name: str, username: str, password: str, bio: str = '',
                    profile_picture: int = None):
        user = self.model(
            email=email,
            name=name,
            username=username,
            password=password,
            bio=bio,
            profile_picture=profile_picture
        )
        user.save()
        return user

    def update_user(self, user_id: int, **kwargs):
        user = self.get(pk=user_id)
        for attr, value in kwargs.items():
            setattr(user, attr, value)
        user.save(using=self._db)
        return user

    def delete_user(self, user_id: int):
        user = self.get(pk=user_id)
        user.delete()


class FollowerManager(models.Manager):
    def add_follower(self, follower: int, followee: int):
        follower = self.model(
            follower=follower,
            followee=followee
        )
        follower.save(using=self._db)
        return follower

    def remove_follower(self, followee_id: int, follower_id: int):
        try:
            follower = self.get(follower_id=follower_id, followee_id=followee_id)
            follower.delete()
        except self.model.DoesNotExist:
            pass


class User(models.Model):
    objects = UserManager()
    email = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=45)
    username = models.CharField(max_length=45, unique=True)
    password = models.CharField(max_length=45)
    bio = models.CharField(max_length=255, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/',
                                        default="/static/images/default_profile_picture.jpg")

    class Meta:
        app_label = 'users'
        db_table = 'user'

    def __str__(self):
        return self.username


class Follower(models.Model):
    objects = FollowerManager()
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')
    followee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')

    class Meta:
        app_label = 'users'
        db_table = 'follower'
        unique_together = ('follower', 'followee')


    def __str__(self):
        return f"{self.follower} -> {self.followee}"
