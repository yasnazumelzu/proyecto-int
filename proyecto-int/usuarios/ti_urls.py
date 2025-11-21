from django.urls import path
from . import ti_views

urlpatterns = [
    path('', ti_views.dashboard_ti, name='dashboard_ti'),
    path('usuarios/', ti_views.lista_usuarios, name='lista_usuarios'),
    path('usuarios/crear/', ti_views.crear_usuario, name='crear_usuario'),
    path('usuarios/<int:id>/editar/', ti_views.editar_usuario, name='editar_usuario'),
    path('usuarios/<int:id>/eliminar/', ti_views.eliminar_usuario, name='eliminar_usuario'),
    path('usuarios/<int:id>/cambiar-estado/', ti_views.cambiar_estado_usuario, name='cambiar_estado_usuario'),
    path('usuarios/<int:id>/resetear-password/', ti_views.resetear_password, name='resetear_password'),
    path('grupos/', ti_views.lista_grupos, name='lista_grupos'),
    path('grupos/<int:id>/', ti_views.detalle_grupo, name='detalle_grupo'),
    path('sesiones/', ti_views.sesiones_activas, name='sesiones_activas'),
    path('sesiones/<str:session_key>/cerrar/', ti_views.cerrar_sesion_usuario, name='cerrar_sesion_usuario'),
    path('estadisticas/', ti_views.estadisticas_sistema, name='estadisticas_sistema'),
]

