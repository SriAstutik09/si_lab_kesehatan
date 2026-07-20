from django.urls import path
from . import views

app_name = 'mahasiswa'

urlpatterns = [
    # Ganti views.dashboard menjadi views.dashboard_view
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('pinjam/', views.pinjam_lab_view, name='pinjam_lab'),
]