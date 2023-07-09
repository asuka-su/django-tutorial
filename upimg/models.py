from django.db import models
from django.contrib.auth.models import User
from PIL import Image, ImageOps
from io import BytesIO
from django.core.files.base import ContentFile
from django.dispatch import receiver
import os

# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

class Photo(models.Model):
    uploader = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='photos/')
    upload_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def scale(self):
        img = Image.open(self.image)
        width, height = img.size
        if height > 300:
            ratio = 300 / height
        else:
            ratio = 1
        img = img.resize((int(width * ratio), int(height * ratio)))
        output = BytesIO()
        img.save(output, format='jpeg', quality=100)
        output.seek(0)
        self.image = ContentFile(output.read(), f'{self.image.name}')
    
@receiver(models.signals.post_delete, sender=Photo)
def auto_delete_image(sender, instance, **kwargs):
    if instance.image:
        if (os.path.isfile(instance.image.path)):
            os.remove(instance.image.path)