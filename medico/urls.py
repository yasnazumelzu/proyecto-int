from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_medico, name='dashboard_medico'),
]
