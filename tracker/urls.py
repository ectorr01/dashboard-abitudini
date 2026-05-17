from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('toggle/<int:abitudine_id>/', views.toggle_abitudine, name='toggle_abitudine'),
    path('aggiungi/', views.aggiungi_abitudine, name='aggiungi_abitudine'),  # ← nuova
]