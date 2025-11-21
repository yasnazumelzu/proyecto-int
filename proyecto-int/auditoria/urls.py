from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_auditoria, name='lista_auditoria'),
    path('<int:id>/', views.detalle_auditoria, name='detalle_auditoria'),
]

