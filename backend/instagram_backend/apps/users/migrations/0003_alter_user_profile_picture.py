# Generated by Django 4.2.2 on 2024-04-02 19:35

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0002_remove_user_profile_picture_id_user_profile_picture"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="profile_picture",
            field=models.ImageField(
                blank=True,
                default="C:\\Users\\oskar\\Downloads\\Telegram Desktop\\photo_2024-04-02_21-18-10.jpg",
                null=True,
                upload_to="profile_pictures/",
            ),
        ),
    ]
