# Generated by Django 5.1.5 on 2025-03-24 18:09

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('list_foods', '0016_foods_store_alter_foods_value_table'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Complements',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Nome')),
                ('qtmin', models.IntegerField(blank=True, null=True, verbose_name='Quantidade min.')),
                ('qtmax', models.IntegerField(blank=True, null=True, verbose_name='Quantidade max.')),
                ('mandatory', models.BooleanField(default=True, verbose_name='Obrigatório')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='complements', to=settings.AUTH_USER_MODEL, verbose_name='Criado por')),
            ],
        ),
        migrations.CreateModel(
            name='ItenComplement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Nome')),
                ('description', models.CharField(max_length=100, verbose_name='Descrição')),
                ('value', models.IntegerField(blank=True, null=True, verbose_name='Valor')),
                ('status', models.BooleanField(default=False, verbose_name='Pausar')),
                ('complements', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='complements', to='list_foods.complements', verbose_name='Complementos')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='ItenComplement', to=settings.AUTH_USER_MODEL, verbose_name='Criado por')),
            ],
        ),
    ]
