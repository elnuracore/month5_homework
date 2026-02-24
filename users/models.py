from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.exceptions import ValidationError

class User(AbstractUser):
    phone_number = models.CharField(max_length=15, blank=True, null=True)

    def clean(self):
        super().clean()
        if self.is_superuser and not self.phone_number:
            raise ValidationError(
                {'phone_number': 'Номер телефона обязателен для суперпользователя.'}
            )

    def __str__(self):
        return self.username

class UserConfirmation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)