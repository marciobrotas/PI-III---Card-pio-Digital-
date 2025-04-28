from django.shortcuts import render, redirect
from .forms import UsuarioForm
from .models import UserWeb

def register_user(request):
    if request.method == 'POST':
        form = UsuarioForm(request.POST)

        # Verificar se o telefone já existe no banco de dados, antes de validar o formulário
        telefone = request.POST.get('telefone')
        usuario_existente = UserWeb.objects.filter(telefone=telefone).first()

        if usuario_existente:
            # Se o usuário já existe, armazena os dados na sessão e redireciona para '/foods/'
            request.session['usuario_id'] = usuario_existente.id
            request.session['nome'] = usuario_existente.nome
            request.session['telefone'] = usuario_existente.telefone
            return redirect('/foods/')  # Redireciona para a página de foods

        if form.is_valid():  # Agora você pode validar o formulário normalmente
            nome = form.cleaned_data['nome']
            telefone = form.cleaned_data['telefone']

            # Criar um novo usuário com os dados do formulário
            usuario = form.save()

            # Armazenar dados na sessão
            request.session['usuario_id'] = usuario.id
            request.session['nome'] = usuario.nome
            request.session['telefone'] = usuario.telefone

            return redirect('/foods/')  # Redireciona para a página de foods

    else:
        form = UsuarioForm()

    return render(request, 'users_web/register.html', {'form': form})
