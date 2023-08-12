from django.db import models
from django.contrib.auth.models import User
from PIL import Image

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(default='profile_pics/default.jpg', upload_to='profile_pics')
    bio = models.TextField(max_length=200, null=True, default=None)
    follower = models.IntegerField(null=True, default=0)

    def __str__(self) -> str:
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # First save the model

        image = Image.open(self.profile_pic.path)

        if image.height > 350 or image.width > 350:
            resized_size = (350, 350)
            image.thumbnail(resized_size)
            image.save(self.profile_pic.path)
