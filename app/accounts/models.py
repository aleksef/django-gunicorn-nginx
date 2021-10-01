from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_delete
from django.dispatch.dispatcher import receiver


class UserImage(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    src = models.ImageField(upload_to='user_images/', default='user_images/user-default.jpg')

    def __str__(self):
        return self.user.username


@receiver(post_delete, sender=UserImage)
def userimage_delete(sender, instance, **kwargs):
    if instance.src != "user_images/user-default.jpg":
        instance.src.delete(False)
