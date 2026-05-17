from django.db import models
from django.contrib.auth.models import User

class Abitudine(models.Model):
    nome = models.CharField(max_length=50)
    proprietario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='abitudini')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome

    class Meta:
        ordering = ['nome']


class LogAbitudine(models.Model):
    abitudine = models.ForeignKey(Abitudine, on_delete=models.CASCADE, related_name='log')
    data = models.DateField()
    completata = models.BooleanField(default=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['abitudine', 'data'], name='unique_daily_log')
        ]
        ordering = ['-data']

    def __str__(self):
        return f"{self.abitudine.nome} - {self.data}"