from django.db import models
from django.conf import settings

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    avatar = models.ImageField(upload_to='avatars/', default='avatars/default.png', blank=True)
    priorities = models.TextField(blank=True, null=True, verbose_name="Приоритеты обучения", 
                                   help_text="Ваши цели и приоритеты в обучении")

    def __str__(self):
        return self.user.username
