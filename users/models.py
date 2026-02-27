from django.db import models
from django.contrib.auth.models import User, AbstractUser
from .managers import CustomUserManager


class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    objects = CustomUserManager()
    
    REQUIRED_FIELDS = ['email', 'phone_number']


class UserConfirmation(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='confirmation_code')
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} - {self.code}'