from django.apps import AppConfig


class ListFoodsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'list_foods'
    verbose_name = 'Cardápio'


# list_foods/apps.py
from django.apps import AppConfig

class ListFoodsConfig(AppConfig):
    name = 'list_foods'
    verbose_name = 'Cardápio'

    def ready(self):
        # Importando o arquivo signals para garantir que o sinal será carregado
        import list_foods.signals
