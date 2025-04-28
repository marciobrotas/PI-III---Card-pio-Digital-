from django.contrib import admin
from delivery_men.models import Delivery_men
from django.apps import apps
from django.core.exceptions import ObjectDoesNotExist

class DeliveryMenAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'phone', 
    ]
    search_fields = ('name',)
    # get_queryset = get_queryset
    # save_model = save_model

    # Filtro para o usuário ver apenas os itens de sua loja
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if request.user.is_superuser:
            return queryset
        return queryset.filter(created_by=request.user)

    def save_model(self, request, obj, form, change):
        Profile = apps.get_model('list_foods', 'Profile')

        if not obj.created_by:
            obj.created_by = request.user  # Preenche automaticamente com o usuário logado

        # Obtém a loja associada ao usuário logado
        try:
            profile = Profile.objects.get(user=request.user)
            obj.store = profile.store  # Associa a loja do perfil ao campo store
        except ObjectDoesNotExist:
            raise ValueError("Nenhuma loja associada ao usuário logado.")  # Lança um erro se não encontrar loja

        obj.save()

        # Para não exibir os campos 'created_by' e 'store' no formulário de edição
    exclude = ('created_by', 'store')

admin.site.register(Delivery_men, DeliveryMenAdmin)