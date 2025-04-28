from django.contrib import admin, messages
from django.apps import apps
from django.urls import reverse
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.core.exceptions import ObjectDoesNotExist
from store_profile.models import (
    StoreInformation, StoreLayout, StoreAddress, StoreOpeningHours,
    StoreFreightPerKilometer, StoreFreightPerDistrict
)

class StoreInformationAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'url', 'phone', 'description', 'minimum_order_delivery',
        'minimum_order_pick_up'
    ]
    search_fields = ('name',)

    # Filtro para o usuário ver apenas os itens de sua loja
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if request.user.is_superuser:
            return queryset
        return queryset.filter(created_by=request.user)

    def save_model(self, request, obj, form, change):
        Profile = apps.get_model('list_foods', 'Profile')
        StoreInformation = apps.get_model('store_profile', 'StoreInformation')

        if not obj.created_by:
            obj.created_by = request.user  # Preenche automaticamente com o usuário logado

        # Obtém a loja associada ao usuário logado
        try:
            profile = Profile.objects.get(user=request.user)
            obj.store = profile.store  # Associa a loja do perfil ao campo store
        except ObjectDoesNotExist:
            raise ValueError("Nenhuma loja associada ao usuário logado.")  # Lança um erro se não encontrar loja

        if not change and StoreInformation.objects.filter(created_by=request.user).exists():
            messages.error(request, "Você já cadastrou um registro e não pode criar outro.")
            return  # Interrompe o salvamento

        obj.save()
        messages.success(request, "Registro salvo com sucesso!")

    def message_user(self, request, *args, **kwargs):
        """Evita que o Django Admin exiba mensagens padrão de sucesso."""
        pass


        # Para não exibir os campos 'created_by' e 'store' no formulário de edição
    exclude = ('created_by',)

admin.site.register(StoreInformation, StoreInformationAdmin)


class StoreLayoutAdmin(admin.ModelAdmin):
    list_display = ['cor', 'photo']
    search_fields = ('cor',)

    # Filtro para o usuário ver apenas os itens de sua loja
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if request.user.is_superuser:
            return queryset
        return queryset.filter(created_by=request.user)

    def save_model(self, request, obj, form, change):
        Profile = apps.get_model('list_foods', 'Profile')
        StoreLayout = apps.get_model('store_profile', 'StoreLayout')

        if not obj.created_by:
            obj.created_by = request.user  # Preenche automaticamente com o usuário logado

        # Obtém a loja associada ao usuário logado
        try:
            profile = Profile.objects.get(user=request.user)
            obj.store = profile.store  # Associa a loja do perfil ao campo store
        except ObjectDoesNotExist:
            raise ValueError("Nenhuma loja associada ao usuário logado.")  # Lança um erro se não encontrar loja

        if not change and StoreLayout.objects.filter(created_by=request.user).exists():
            messages.error(request, "Você já cadastrou um registro e não pode criar outro.")
            return  # Interrompe o salvamento

        obj.save()
        messages.success(request, "Registro salvo com sucesso!")

    def message_user(self, request, *args, **kwargs):
        """Evita que o Django Admin exiba mensagens padrão de sucesso."""
        pass


        # Para não exibir os campos 'created_by' e 'store' no formulário de edição
    exclude = ('created_by',)

admin.site.register(StoreLayout, StoreLayoutAdmin)


class StoreAddressAdmin(admin.ModelAdmin):
    list_display = [
        'cep', 'address', 'number', 'add_ons', 'district', 'city'
    ]
    search_fields = ('address',)

    # Filtro para o usuário ver apenas os itens de sua loja
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if request.user.is_superuser:
            return queryset
        return queryset.filter(created_by=request.user)

    def save_model(self, request, obj, form, change):
        Profile = apps.get_model('list_foods', 'Profile')
        StoreAddress = apps.get_model('store_profile', 'StoreAddress')  

        if not obj.created_by:
            obj.created_by = request.user

        try:
            profile = Profile.objects.get(user=request.user)
            obj.store = profile.store
        except ObjectDoesNotExist:
            messages.error(request, "Nenhuma loja está associada à sua conta.")
            return  # Interrompe o salvamento

        if not change and StoreAddress.objects.filter(created_by=request.user).exists():
            messages.error(request, "Você já cadastrou um registro e não pode criar outro.")
            return  # Interrompe o salvamento

        obj.save()
        messages.success(request, "Registro salvo com sucesso!")

    def message_user(self, request, *args, **kwargs):
        """Evita que o Django Admin exiba mensagens padrão de sucesso."""
        pass

admin.site.register(StoreAddress, StoreAddressAdmin)

class StoreOpeningHoursAdmin(admin.ModelAdmin):
    list_display = [
        'close_now', 'TimeZone', 'monday_open', 'monday_close', 'tuesday_open',
        'tuesday_close', 'wednesday_open', 'wednesday_close', 'thursday_open',
        'thursday_close', 'friday_open', 'friday_close', 'saturday_open',
        'saturday_close', 'sunday_open', 'sunday_close'
    ]
    search_fields = ('close_now',)

    # Filtro para o usuário ver apenas os itens de sua loja
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if request.user.is_superuser:
            return queryset
        return queryset.filter(created_by=request.user)

    def save_model(self, request, obj, form, change):
        Profile = apps.get_model('list_foods', 'Profile')
        StoreOpeningHours = apps.get_model('store_profile', 'StoreOpeningHours')  

        if not obj.created_by:
            obj.created_by = request.user  # Preenche automaticamente com o usuário logado

        # Obtém a loja associada ao usuário logado
        try:
            profile = Profile.objects.get(user=request.user)
            obj.store = profile.store  # Associa a loja do perfil ao campo store
        except ObjectDoesNotExist:
            raise ValueError("Nenhuma loja associada ao usuário logado.")  # Lança um erro se não encontrar loja

        if not change and StoreOpeningHours.objects.filter(created_by=request.user).exists():
            messages.error(request, "Você já cadastrou um registro e não pode criar outro.")
            return  # Interrompe o salvamento

        obj.save()
        messages.success(request, "Registro salvo com sucesso!")

    def message_user(self, request, *args, **kwargs):
        """Evita que o Django Admin exiba mensagens padrão de sucesso."""
        pass

        # Para não exibir os campos 'created_by' e 'store' no formulário de edição
    exclude = ('created_by',)

admin.site.register(StoreOpeningHours, StoreOpeningHoursAdmin)


class StoreFreightPerKilometerAdmin(admin.ModelAdmin):
    list_display = ['distance', 'times', 'value']

    def render_change_form(self, request, context, add=False, change=False, form_url='', obj=None):
        Profile = apps.get_model('list_foods', 'Profile')
        StoreFreightPerDistrict = apps.get_model('store_profile', 'StoreFreightPerDistrict')

        # Verifica se há dados na outra tabela
        if add and StoreFreightPerDistrict.objects.filter(created_by=request.user).exists():
            # Adiciona mensagem de aviso
            messages.warning(request, "Existem registros cadastrados por bairro. Se registrar por kilometro, todos os registros de bairros serao apagados")

            # Armazena no contexto a URL de confirmação
            context['has_other_data'] = True
            context['other_data_url'] = reverse('admin:store_profile_storefreightperdistrict_changelist')

        return super().render_change_form(request, context, add, change, form_url, obj)

    def save_model(self, request, obj, form, change):
        Profile = apps.get_model('list_foods', 'Profile')
        StoreFreightPerDistrict = apps.get_model('store_profile', 'StoreFreightPerDistrict')
        StoreFreightPerKilometer = apps.get_model('store_profile', 'StoreFreightPerKilometer')

        # Garante que o campo `created_by` seja atribuído automaticamente
        if not obj.created_by:
            obj.created_by = request.user

        # Obtém a loja associada ao usuário logado
        try:
            profile = Profile.objects.get(user=request.user)
            obj.store = profile.store
        except ObjectDoesNotExist:
            raise ValueError("Nenhuma loja associada ao usuário logado.")

        # if not change and StoreOpeningHours.objects.filter(created_by=request.user).exists():
        #     messages.error(request, "Você já cadastrou um registro e não pode criar outro.")
        #     return  # Interrompe o salvamento
        
        # Excluir registros da outra tabela após confirmação
        if StoreFreightPerDistrict.objects.filter(created_by=request.user).exists():
            StoreFreightPerDistrict.objects.filter(created_by=request.user).delete()

        obj.save()
        # messages.success(request, "Registro salvo com sucesso!")

    # def message_user(self, request, *args, **kwargs):
    #     """Evita que o Django Admin exiba mensagens padrão de sucesso."""
    #     pass

    exclude = ('created_by',)

admin.site.register(StoreFreightPerKilometer, StoreFreightPerKilometerAdmin)


class StoreFreightPerDistrictAdmin(admin.ModelAdmin):
    list_display = ['cit', 'district', 'times', 'value']

    def render_change_form(self, request, context, add=False, change=False, form_url='', obj=None):
        Profile = apps.get_model('list_foods', 'Profile')
        StoreFreightPerKilometer = apps.get_model('store_profile', 'StoreFreightPerKilometer')
        StoreFreightPerDistrict = apps.get_model('store_profile', 'StoreFreightPerDistrict')

        # Verifica se há dados na tabela StoreFreightPerKilometer
        if add and StoreFreightPerKilometer.objects.filter(created_by=request.user).exists():
            # Adiciona mensagem de aviso
            messages.warning(request, "Existem registros cadastrados por quilômetro. Se registrar por bairro, todos os registros de kilometros serao apagados")

            # Armazena no contexto a URL de confirmação
            context['has_other_data'] = True
            context['other_data_url'] = reverse('admin:store_profile_storefreightperkilometer_changelist')

        return super().render_change_form(request, context, add, change, form_url, obj)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if request.user.is_superuser:
            return queryset
        return queryset.filter(created_by=request.user)

    def save_model(self, request, obj, form, change):
        Profile = apps.get_model('list_foods', 'Profile')
        StoreFreightPerKilometer = apps.get_model('store_profile', 'StoreFreightPerKilometer')

        # Garante que o campo `created_by` seja atribuído automaticamente
        if not obj.created_by:
            obj.created_by = request.user

        # Obtém a loja associada ao usuário logado
        try:
            profile = Profile.objects.get(user=request.user)
            obj.store = profile.store
        except ObjectDoesNotExist:
            raise ValueError("Nenhuma loja associada ao usuário logado.")

        # if not change and StoreFreightPerDistrict.objects.filter(created_by=request.user).exists():
        #     messages.error(request, "Você já cadastrou um registro e não pode criar outro.")
        #     return  # Interrompe o salvamento
        
        # Excluir registros da tabela StoreFreightPerKilometer após confirmação
        if StoreFreightPerKilometer.objects.filter(created_by=request.user).exists():
            StoreFreightPerKilometer.objects.filter(created_by=request.user).delete()

        obj.save()
        messages.success(request, "Registro salvo com sucesso!")

    def message_user(self, request, *args, **kwargs):
        """Evita que o Django Admin exiba mensagens padrão de sucesso."""
        pass

    exclude = ('created_by',)

admin.site.register(StoreFreightPerDistrict, StoreFreightPerDistrictAdmin)
