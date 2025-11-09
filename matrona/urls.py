from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_matrona, name='dashboard_matrona'),
]
