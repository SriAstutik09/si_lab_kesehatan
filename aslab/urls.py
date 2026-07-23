from django.urls import path
from . import views

app_name = 'aslab'

urlpatterns = [
    # Dashboard ASLAB
    path('dashboard/', views.dashboard_aslab, name='dashboard'),
    
    # Rute Aksi Verifikasi / Tolak / Selesai
    path('verifikasi/<int:pinjam_id>/<str:aksi>/', views.verifikasi_peminjaman, name='verifikasi'),
    # path LAPORAN 
    path('laporan/', views.laporan_peminjaman, name='laporan'),
]
