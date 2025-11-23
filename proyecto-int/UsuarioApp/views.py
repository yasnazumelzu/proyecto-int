from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib.auth import get_user_model

User = get_user_model()

@login_required
@user_passes_test(es_admin)
def listar_usuarios(request):
    usuarios = User.objects.select_related('perfil').order_by('username')
    paginator = Paginator(usuarios, 10)  # 10 por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, "usuarios/listar_usuarios.html", {"page_obj": page_obj})

@login_required
def listar_usuarios_simple(request):
    lista = User.objects.all().order_by("username")
    paginator = Paginator(lista, 10)
    page = request.GET.get("page")
    usuarios = paginator.get_page(page)
    return render(request, "usuarios/lista.html", {"usuarios": usuarios})
