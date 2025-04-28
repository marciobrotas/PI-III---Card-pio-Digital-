from django.db import models

class UserWeb(models.Model):
    nome = models.CharField(max_length=100)
    telefone = models.CharField(max_length=15, unique=True)

    def __str__(self):
        return self.nome
