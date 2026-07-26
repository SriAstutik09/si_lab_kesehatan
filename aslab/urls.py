from django.urls import path
from . import views

app_name = 'aslab'

urlpatterns = [
    # Dashboard & Verifikasi Peminjaman
    path('dashboard/', views.dashboard_aslab, name='dashboard'),
    path('peminjaman/<int:pinjam_id>/<str:aksi>/', views.verifikasi_peminjaman, name='verifikasi_peminjaman'),
    
    # Laporan
    path('laporan/', views.laporan_peminjaman, name='laporan'),
    
    # Verifikasi Akun MHS
    path('verifikasi-akun/', views.verifikasi_akun_mhs, name='verifikasi_akun'),
    path('proses-akun/<int:user_id>/<str:aksi>/', views.proses_persetujuan_akun, name='proses_persetujuan_akun'),

    # ==========================================
    # ROUTE MASTER DATA (RUANG & ALAT/BAHAN)
    # ==========================================
    path('master-data/', views.master_data, name='master_data'),
    
    # CRUD Ruang
    path('master-data/ruang/tambah/', views.tambah_ruang, name='tambah_ruang'),
    path('master-data/ruang/edit/<int:id>/', views.edit_ruang, name='edit_ruang'),
    path('master-data/ruang/hapus/<int:id>/', views.hapus_ruang, name='hapus_ruang'),

    # CRUD Alat/Bahan
    path('master-data/alat/tambah/', views.tambah_alat, name='tambah_alat'),
    path('master-data/alat/edit/<int:id>/', views.edit_alat, name='edit_alat'),
    path('master-data/alat/hapus/<int:id>/', views.hapus_alat, name='hapus_alat'),
]