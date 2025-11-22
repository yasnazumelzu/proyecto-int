from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render
from django.contrib.auth.models import User

def es_admin(user):
    return user.is_superuser or getattr(user.perfil, 'rol', '') == 'ADMIN'

@login_required
@user_passes_test(es_admin)
def listar_usuarios(request):
    usuarios = User.objects.select_related('perfil').order_by('username')
    paginator = Paginator(usuarios, 10)  # 10 por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, "usuarios/listar_usuarios.html", {"page_obj": page_obj})
