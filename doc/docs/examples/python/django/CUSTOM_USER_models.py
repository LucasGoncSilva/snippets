from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class User(AbstractUser):
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    email: object = models.EmailField(unique=True)


class ActivationAccountToken(models.Model):
    value: object = models.CharField(max_length=128)
    used: object = models.BooleanField(default=False, verbose_name='Usado?')
    created: object = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Token de Ativação'
        verbose_name_plural = 'Tokens de Ativação'

    def __str__(self) -> str:
        return f'{self.value}'
