from django.urls import path
from . import views

app_name = 'aslab'

urlpatterns = [
    path('dashboard/', views.dashboard_aslab, name='dashboard'),
]