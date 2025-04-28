# list_foods/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile  # Certifique-se de que o Profile está no seu models.py

# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#     # Cria o Profile automaticamente quando o usuário é criado
#     if created:
#         Profile.objects.create(user=instance)

# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     # Salva o Profile caso ele já exista (atualiza se necessário)
#     instance.profile.save()


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:  # Somente cria o perfil se o usuário foi criado
        # Verifica se o perfil já existe antes de criar um novo
        if not hasattr(instance, 'profile'):
            Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    # Isso é opcional, mas garante que o perfil seja salvo quando o usuário for salvo
    instance.profile.save()