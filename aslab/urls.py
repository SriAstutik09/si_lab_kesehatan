from django.urls import path
from . import views

app_name = 'aslab'

urlpatterns = [
    # 1. Dashboard ASLAB
    path('dashboard/', views.dashboard_aslab, name='dashboard'),
    
    # 2. Rute Aksi Verifikasi / Tolak / Selesai Peminjaman Lab
    path('verifikasi/<int:pinjam_id>/<str:aksi>/', views.verifikasi_peminjaman, name='verifikasi'),
    
    # 3. Path LAPORAN 
    path('laporan/', views.laporan_peminjaman, name='laporan'),

    # RUTE BARU: VERIFIKASI AKUN MAHASISWA BARU
    path('verifikasi-akun/', views.verifikasi_akun_mhs, name='verifikasi_akun'),
    path('proses-akun/<int:user_id>/<str:aksi>/', views.proses_persetujuan_akun, name='proses_persetujuan_akun'),
]