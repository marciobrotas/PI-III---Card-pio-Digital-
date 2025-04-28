from django.shortcuts import render, redirect
from list_foods.models import Foods
from itertools import groupby
from datetime import datetime
from .models import UserWeb

def foods_viwer(request):
    usuario_id = request.session.get('usuario_id')
    if usuario_id:
        # Obter o dia da semana e a hora atual
        now = datetime.now()
        current_day = now.strftime('%A').lower()  # 'monday', 'tuesday', etc.
        current_time = now.time()

        # Mapeamento de dias da semana para os campos no modelo
        day_mapping = {
            'monday': ('monday_open', 'monday_close'),
            'tuesday': ('tuesday_open', 'tuesday_close'),
            'wednesday': ('wednesday_open', 'wednesday_close'),
            'thursday': ('thursday_open', 'thursday_close'),
            'friday': ('friday_open', 'friday_close'),
            'saturday': ('saturday_open', 'saturday_close'),
            'sunday': ('sunday_open', 'sunday_close'),
        }

        open_field, close_field = day_mapping[current_day]

        # Filtrar alimentos disponíveis no dia e horário
        foods = Foods.objects.all()
        # foods = Foods.objects.filter(
        #     **{
        #         f'{open_field}__lte': current_time,  # Abertura menor ou igual ao horário atual
        #         f'{close_field}__gte': current_time  # Fechamento maior ou igual ao horário atual
        #     }
        # )

        # Filtrar por nome, se houver busca
        search = request.GET.get('search')
        if search:
            foods = foods.filter(name__icontains=search)

        # Agrupar alimentos por categoria
        grouped_foods = {category: list(group) for category, group in groupby(foods, lambda x: x.category)}

        # Agora, podemos passar tanto os alimentos agrupados quanto os complementos e seus itens para o template
        return render(request, 'list_foods.html', {
            'grouped_foods': grouped_foods
        })
    else:
        return redirect('/register/')
