from django.urls import path
from django.shortcuts import redirect
from . import views

# Namespace aplikasi 'mahasiswa' agar pemanggilan URL lebih rapi (contoh: 'mahasiswa:dashboard')
app_name = 'mahasiswa'

urlpatterns = [
    # 1. Pengalihan Otomatis: Jika user mengetik /mahasiswa/, langsung dilempar ke /mahasiswa/dashboard/
    path('', lambda request: redirect('mahasiswa:dashboard')),
    
    # 2. Halaman Utama Dashboard Mahasiswa
    path('dashboard/', views.dashboard_view, name='dashboard'),
    
    # 3. Halaman Form Pengajuan Peminjaman
    path('pinjam/', views.pinjam_lab_view, name='pinjam_lab'),
    
    # 4. Rute Aksi Pengembalian Alat/Lab (Mengirimkan parameter ID peminjaman <int:pinjam_id>)
    path('kembalikan/<int:pinjam_id>/', views.ajukan_pengembalian_view, name='ajukan_pengembalian'),
]