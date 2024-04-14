import os
from django.db import models
from apps.users.models import User


class ContentManager(models.Manager):
    def create_content(self, content_type: str):
        content = self.model(
            type=content_type
        )
        content.save()
        return content

    def delete_content(self, content_id):
        content = self.get(pk=content_id)
        content.delete()


class VideoManager(models.Manager):
    def create_video(self, user_id: int, video_file):
        last_video = self.order_by('-video_id').first()
        if last_video:
            last_video_id = last_video.video_id
        else:
            last_video_id = 0

        video_id = last_video_id + 1

        video = self.model(
            user_id=user_id,
            video_id=video_id
        )
        video.save()

        user_video_path = os.path.join('media', 'video', str(user_id))

        os.makedirs(user_video_path, exist_ok=True)

        video_file_path = os.path.join(user_video_path, str(video_id))
        with open(video_file_path, 'wb') as f:
            for chunk in video_file.chunks():
                f.write(chunk)

        return video

    def delete_video(self, video_id: int):
        video = self.get(pk=video_id)
        video_path = os.path.join('media', 'video', str(video.user_id), str(video.video_id))
        if os.path.exists(video_path):
            os.remove(video_path)
        video.delete()


class PhotoManager(models.Manager):
    pass


class StoryManager(models.Manager):
    pass


class DirectMessageManager(models.Manager):
    pass


class Content(models.Model):
    TYPE_CHOICES = (
        ("Story", 'story'),
        ("Post", 'post')
    )

    objects = ContentManager
    type = models.CharField(max_length=5, choices=TYPE_CHOICES)

    class Meta:
        app_label = 'contents'
        db_table = 'content'


class Video(models.Model):
    objects = VideoManager
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    video_path_id = models.IntegerField()

    class Meta:
        app_label = 'contents'
        db_table = 'video'
        unique_together = ('user', 'video_path_id')


class Photo(models.Model):
    objects = PhotoManager
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    photo_path_id = models.IntegerField()

    class Meta:
        app_label = 'contents'
        db_table = 'photo'
        unique_together = ('user', 'photo_path_id')


class Story(models.Model):
    objects = StoryManager
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.ForeignKey(Content, on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)

    class Meta:
        app_label = 'contents'
        db_table = 'story'


class DirectMessage(models.Model):
    TYPE_CHOICES = (
        ('Content', 'content'),
        ('Video', 'video'),
        ('Photo', 'photo'),
        ('Text', 'text')
    )
    objects = DirectMessageManager
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    content = models.ForeignKey(Content, on_delete=models.CASCADE, null=True, blank=True)
    video = models.ForeignKey(Video, on_delete=models.CASCADE, null=True, blank=True)
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE, null=True, blank=True)
    text = models.CharField(max_length=1024, null=True, blank=True)
    created_at = models.DateTimeField()
    type = models.CharField(max_length=7, choices=TYPE_CHOICES)

    class Meta:
        app_label = 'contents'
        db_table = 'direct_message'