from django.contrib import admin
from list_foods.models import Foods, Category, DiaSemana, Store, Complements, ItenComplement
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from .models import Profile # Importe o Profile aqui

from django.core.exceptions import ObjectDoesNotExist
# from list_foods_profile.models import ListFoodsProfile  # Im

class CategoryAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'monday_open', 'monday_close',  'tuesday_open',
        'tuesday_close', 'wednesday_open', 'wednesday_close', 'thursday_open',
        'thursday_close', 'friday_open', 'friday_close', 'saturday_open',
        'saturday_close', 'sunday_open', 'sunday_close', 'store', 'created_by'
    ]
    search_fields = ('name',)
    

    def clear_name(self, request):
        categorys = Category().get('name')
        print(categorys)
    # Filtro para o usuário ver apenas os itens de sua loja
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if request.user.is_superuser:
            return queryset
        return queryset.filter(created_by=request.user)
    
    
    def save_model(self, request, obj, form, change):
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

# Admin para Item de Comida (Foods)
class FoodsAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'category', 'value_delivery', 'value_table', 'short_description',  # Altere para 'short_description' em vez de 'description'
        'monday_open', 'monday_close', 'tuesday_open', 'tuesday_close', 'wednesday_open', 'wednesday_close',
        'thursday_open', 'thursday_close', 'friday_open', 'friday_close', 'saturday_open', 'saturday_close',
        'sunday_open', 'sunday_close', 'status', 'delivery', 'table', 'created_by', 'modification_date'
    )
    
    search_fields = ('name',)

    def short_description(self, obj):
        """Limita o campo description a 15 caracteres."""
        return obj.description[:15] + "..." if len(obj.description) > 15 else obj.description

    short_description.short_description = "Descrição"  # Nome da coluna no Admin
    
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if request.user.is_superuser:
            return queryset
        return queryset.filter(created_by=request.user)

    def save_model(self, request, obj, form, change):
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



# Admin para a loja
class StoreAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'cnpj')
    search_fields = ('name', 'cnpj')
    
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if request.user.is_superuser:
            return queryset
        return queryset.filter(owner=request.user)  # Relacionando a loja com o usuário logado

# Complemento para itens
class ComplementsAdmin(admin.ModelAdmin):
    list_display = ('name', 'qtmin', 'qtmax', 'mandatory')
    search_fields = ('name',)
    
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if request.user.is_superuser:
            return queryset
        return queryset.filter(created_by=request.user)  # Relacionando a loja com o usuário logado
    
    def save_model(self, request, obj, form, change):
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
    
# Itens para complemento
class ItenComplementAdmin(admin.ModelAdmin):
    list_display = ('complements', 'name', 'description', 'value', 'status')
    search_fields = ('complements','name',)
    
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if request.user.is_superuser:
            return queryset
        return queryset.filter(created_by=request.user)  # Relacionando a loja com o usuário logado

    def save_model(self, request, obj, form, change):
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
    
# Formulário para customizar a criação/edição do usuário
class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Perfil'
    fk_name = 'user'

# Customizando o admin do User
class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline,)  # Incluindo o perfil na edição do usuário
    
    # Personalizando os campos a serem exibidos na listagem
    list_display = ('username', 'email', 'first_name', 'last_name', 'store', 'is_staff', 'is_active')
    
    # Personalizando o formulário de edição do usuário
    def store(self, obj):
        return obj.profile.store.name if obj.profile and obj.profile.store else 'Nenhuma loja'


# Filtro para o usuário ver apenas os itens de sua loja
def get_queryset(self, request):
    queryset = super().get_queryset(request)
    if request.user.is_superuser:
        return queryset
    return queryset.filter(created_by=request.user)

# Registrando o modelo `User` com a customização do admin
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

# Registrando os modelos no Admin
admin.site.register(Category, CategoryAdmin)
admin.site.register(Foods, FoodsAdmin)
admin.site.register(Store, StoreAdmin)
admin.site.register(Complements, ComplementsAdmin)
admin.site.register(ItenComplement, ItenComplementAdmin)

# Personalizando o cabeçalho do admin
admin.site.site_header = "Painel de Gerenciamento" 
admin.site.site_title = "Título da Página do Admin"
admin.site.index_title = "Bem-vindo ao Painel de Administração"
