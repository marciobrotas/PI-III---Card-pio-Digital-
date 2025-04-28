from django.db import models
from django.contrib.auth.models import User

class Delivery_men(models.Model):
    name = models.CharField(verbose_name='Nome', max_length=200)
    phone = models.ImageField(upload_to='img_delivery_men/', blank=True, null=True)
    created_by = models.ForeignKey(
        User,
        verbose_name='Criado por',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = 'Entregadores'
        verbose_name_plural = 'Entregadores'

    def __str__(self):
        return self.name