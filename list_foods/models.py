from django.db import models
from django.contrib.auth.models import User
from datetime import time
from decimal import Decimal

# Definindo o modelo DiaSemana para os dias da semana
class DiaSemana(models.Model):
    DIA_CHOICES = [
        ('seg', 'Segunda-feira'),
        ('ter', 'Terça-feira'),
        ('qua', 'Quarta-feira'),
        ('qui', 'Quinta-feira'),
        ('sex', 'Sexta-feira'),
        ('sab', 'Sábado'),
        ('dom', 'Domingo'),
    ]
    
    dia = models.CharField(max_length=3, choices=DIA_CHOICES, unique=True)

    def __str__(self):
        return self.get_dia_display()

# Modelo para a loja
class Store(models.Model):
    name = models.CharField(verbose_name='Nome da Loja', max_length=200)
    owner = models.CharField(verbose_name='Proprietário', max_length=200)
    address = models.CharField(verbose_name='Endereço', max_length=300, blank=True, null=True)
    phone = models.CharField(verbose_name='Telefone', max_length=20, blank=True, null=True)
    cnpj = models.CharField(verbose_name='CNPJ', max_length=18, blank=True, null=True)  # Novo campo CNPJ
    creation_date = models.DateTimeField(auto_now_add=True, verbose_name='Data de Criação')
    modification_date = models.DateTimeField(auto_now=True, verbose_name='Última Modificação')
    active = models.BooleanField(verbose_name='Ativo', default=True)
    created_by = models.ForeignKey(
    User, 
    verbose_name='Criado por', 
    on_delete=models.SET_NULL, 
    null=True, 
    blank=True
    )

    class Meta:
        verbose_name = 'Loja'
        verbose_name_plural = 'Lojas'

    def __str__(self):
        return self.name

# Modelo de Categoria com a relação com a loja
class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(verbose_name='Nome', max_length=200)
    store = models.ForeignKey(Store, verbose_name='Loja', on_delete=models.CASCADE, related_name='categories')  # Relação com a loja
    
    MEAL_TYPE_CHOICES = [
        ('padrao', 'Padrão'),
        ('pizza', 'Pizza'),
    ]

    # Campo com opções de escolha (radiobox no admin)
    meal_type = models.CharField(
        max_length=10,
        verbose_name='Modelo da categoria',
        choices=MEAL_TYPE_CHOICES,
        default='padrao',  # Valor padrão
    )

    monday_open = models.TimeField(verbose_name='Segunda abertura', null=True, blank=True, default=time(0, 0))  # Hora de abertura para segunda-feira
    monday_close = models.TimeField(verbose_name='Segunda fechamento', null=True, blank=True, default=time(0, 0))  # Hora de fechamento para segunda-feira

    tuesday_open = models.TimeField(verbose_name='Terça abertura', null=True, blank=True, default=time(0, 0))  # Hora de abertura para terça-feira
    tuesday_close = models.TimeField(verbose_name='Terça fechamento', null=True, blank=True, default=time(0, 0))  # Hora de fechamento para terça-feira

    wednesday_open = models.TimeField(verbose_name='Quarta abertura', null=True, blank=True, default=time(0, 0))  # Hora de abertura para quarta-feira
    wednesday_close = models.TimeField(verbose_name='Quarta fechamento', null=True, blank=True, default=time(0, 0))  # Hora de fechamento para quarta-feira

    thursday_open = models.TimeField(verbose_name='Quinta abertura', null=True, blank=True, default=time(0, 0))  # Hora de abertura para quinta-feira
    thursday_close = models.TimeField(verbose_name='Quinta fechamento', null=True, blank=True, default=time(0, 0))  # Hora de fechamento para quinta-feira

    friday_open = models.TimeField(verbose_name='Sexta abertura', null=True, blank=True, default=time(0, 0))  # Hora de abertura para sexta-feira
    friday_close = models.TimeField(verbose_name='Sexta fechamento', null=True, blank=True, default=time(0, 0))  # Hora de fechamento para sexta-feira

    saturday_open = models.TimeField(verbose_name='Sábado abertura', null=True, blank=True, default=time(0, 0))  # Hora de abertura para sábado
    saturday_close = models.TimeField(verbose_name='Sábado fechamento', null=True, blank=True, default=time(0, 0))  # Hora de fechamento para sábado

    sunday_open = models.TimeField(verbose_name='Domingo abertura', null=True, blank=True, default=time(0, 0))  # Hora de abertura para domingo
    sunday_close = models.TimeField(verbose_name='Domingo fechamento', null=True, blank=True, default=time(0, 0))  # Hora de fechamento para domingo
   # Campo para armazenar o ID do superusuário que criou ou alterou o item
    created_by = models.ForeignKey(User, verbose_name='Criado por', on_delete=models.SET_NULL, null=True, blank=True, related_name='Store')
        
    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'
    
    def __str__(self):
        return self.name

class Complements(models.Model):
    name = models.CharField(max_length=100, verbose_name='Nome')
    qtmin = models.IntegerField(blank=True, verbose_name='Quantidade min.', null=True)
    qtmax = models.IntegerField(blank=True, verbose_name='Quantidade max.', null=True)
    mandatory = models.BooleanField(verbose_name='Obrigatório', default=True)
    # Campo para armazenar o ID do superusuário que criou ou alterou o item
    created_by = models.ForeignKey(User, verbose_name='Criado por', on_delete=models.SET_NULL, null=True, blank=True, related_name='complements')

    class Meta:
        verbose_name = 'Complemento'
        verbose_name_plural = 'Complementos'

    def __str__(self):
        return self.name
    
class ItenComplement(models.Model):
    complements = models.ForeignKey(Complements, verbose_name='Complementos', on_delete=models.PROTECT, related_name='iten_complements')
    name = models.CharField(max_length=100, verbose_name='Nome')
    description = models.TextField(max_length=500, verbose_name='Descrição', blank=True)
    value = models.IntegerField(blank=True, verbose_name='Valor', null=True)
    status = models.BooleanField(verbose_name='Pausar', default=False)  # Valor padrão True
    # Campo para armazenar o ID do superusuário que criou ou alterou o item
    created_by = models.ForeignKey(User, verbose_name='Criado por', on_delete=models.SET_NULL, null=True, blank=True, related_name='ItenComplement')
    
    class Meta:
        verbose_name = 'Item para (Complementos)'
        verbose_name_plural = 'Itens para (Complementos)'

    def __str__(self):
        return self.name
    
# Modelo de Item (Food) com a relação com a loja e categoria
class Foods(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(verbose_name='Nome', max_length=200)
    category = models.ForeignKey(Category, verbose_name='Categoria', on_delete=models.PROTECT, related_name='foods')  # Relação com a categoria
    complement = models.ForeignKey(Complements, verbose_name='Complemento', on_delete=models.PROTECT, related_name='foods_complements')  # Relação com a categoria
    value_delivery = models.IntegerField(blank=True, verbose_name='Preço delivery', null=True)
    value_table = models.IntegerField(blank=True, verbose_name='Preço mesa', null=True, default=1)
    description = models.TextField(verbose_name='Descrição', max_length=500)
    photo = models.ImageField(upload_to='img_foods/', blank=True, null=True)
    store = models.ForeignKey(Store, verbose_name='Loja', on_delete=models.CASCADE, related_name='foods')  # Relação com a loja
    monday_open = models.TimeField(verbose_name='Segunda abertura', null=True, blank=True, default=time(0, 0))  # Hora de abertura para segunda-feira
    monday_close = models.TimeField(verbose_name='Segunda fechamento', null=True, blank=True, default=time(0, 0))  # Hora de fechamento para segunda-feira

    tuesday_open = models.TimeField(verbose_name='Terça abertura', null=True, blank=True, default=time(0, 0))  # Hora de abertura para terça-feira
    tuesday_close = models.TimeField(verbose_name='Terça fechamento', null=True, blank=True, default=time(0, 0))  # Hora de fechamento para terça-feira

    wednesday_open = models.TimeField(verbose_name='Quarta abertura', null=True, blank=True, default=time(0, 0))  # Hora de abertura para quarta-feira
    wednesday_close = models.TimeField(verbose_name='Quarta fechamento', null=True, blank=True, default=time(0, 0))  # Hora de fechamento para quarta-feira

    thursday_open = models.TimeField(verbose_name='Quinta abertura', null=True, blank=True, default=time(0, 0))  # Hora de abertura para quinta-feira
    thursday_close = models.TimeField(verbose_name='Quinta fechamento', null=True, blank=True, default=time(0, 0))  # Hora de fechamento para quinta-feira

    friday_open = models.TimeField(verbose_name='Sexta abertura', null=True, blank=True, default=time(0, 0))  # Hora de abertura para sexta-feira
    friday_close = models.TimeField(verbose_name='Sexta fechamento', null=True, blank=True, default=time(0, 0))  # Hora de fechamento para sexta-feira

    saturday_open = models.TimeField(verbose_name='Sábado abertura', null=True, blank=True, default=time(0, 0))  # Hora de abertura para sábado
    saturday_close = models.TimeField(verbose_name='Sábado fechamento', null=True, blank=True, default=time(0, 0))  # Hora de fechamento para sábado

    sunday_open = models.TimeField(verbose_name='Domingo abertura', null=True, blank=True, default=time(0, 0))  # Hora de abertura para domingo
    sunday_close = models.TimeField(verbose_name='Domingo fechamento', null=True, blank=True, default=time(0, 0))  # Hora de fechamento para domingo

    delivery = models.BooleanField(verbose_name='Delivery', default=True)  # Valor padrão True
    status = models.BooleanField(verbose_name='Pausar', default=False)  # Valor padrão True
    table = models.BooleanField(verbose_name='Mesa', default=False)  # Valor padrão False
    
    # Campo para armazenar o ID do superusuário que criou ou alterou o item
    created_by = models.ForeignKey(User, verbose_name='Criado por', on_delete=models.SET_NULL, null=True, blank=True, related_name='foods_criados')
    
    # Campo para armazenar a data da última modificação
    modification_date = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Item para (Categoria)'
        verbose_name_plural = 'Itens para (Categorias)'

    def __str__(self):
        return self.name

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    store = models.ForeignKey(Store, on_delete=models.CASCADE, null=True, blank=True)  # Campo para associar a loja

    def __str__(self):
        return self.user.username
    
class UserWeb(models.Model):
    nome = models.CharField(max_length=100)
    telefone = models.CharField(max_length=20)
    endereco = models.TextField(blank=True, null=True)  # Pode ser preenchido depois
    data_cadastro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome
