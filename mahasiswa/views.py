# ==============================================================================
# IMPOR MODUL DAN DEPENDENSI DJANGO
# ==============================================================================
# render: Untuk menampilkan file HTML template dengan membawa data (context)
# redirect: Untuk mengarahkan (mengarahkan ulang) halaman web ke URL lain
# get_object_or_404: Mengambil data dari database berdasarkan ID, jika tidak ketemu langsung tampilkan error 404 (aman dari error sistem)
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

# login_required: Hiasan (decorator) untuk mengamankan halaman agar hanya bisa dibuka jika user sudah login
from django.contrib import messages

# Impor model database yang digunakan dalam aplikasi
from core_auth.models import Peminjaman, RuangLab, AlatBahan

# Impor form HTML bawaan Django yang sudah kita definisikan di forms.py
from .forms import PeminjamanForm


# ==============================================================================
# 1. VIEW DASHBOARD MAHASISWA
# ==============================================================================
@login_required(login_url='core_auth:login')
def dashboard_view(request):
    """
    Fungsi untuk menampilkan statistik ringkasan dan daftar riwayat
    peminjaman khusus milik mahasiswa yang sedang login.
    """
    # Mengambil semua daftar peminjaman milik user yang login, diurutkan dari yang terbaru (-tanggal_pinjam)
    jadwal_mahasiswa = Peminjaman.objects.filter(mahasiswa=request.user).order_by('-tanggal_pinjam')
    
    # Menghitung statistik status peminjaman milik user ini
    total_menunggu = Peminjaman.objects.filter(mahasiswa=request.user, status__in=['pending', 'verified']).count()
    total_disetujui = Peminjaman.objects.filter(mahasiswa=request.user, status='disetujui').count()
    total_ditolak = Peminjaman.objects.filter(mahasiswa=request.user, status='ditolak').count()
    
    # Membungkus data ke dalam dictionary context untuk dikirim ke file HTML dashboard.html
    context = {
        'jadwal_mahasiswa': jadwal_mahasiswa,
        'total_menunggu': total_menunggu,
        'total_disetujui': total_disetujui,
        'total_ditolak': total_ditolak,
    }
    return render(request, 'mahasiswa/dashboard.html', context)


# ==============================================================================
# 2. VIEW FORM PINJAM LAB / ALAT
# ==============================================================================
@login_required(login_url='core_auth:login')
def pinjam_lab_view(request):
    """
    Fungsi untuk menampilkan form pengajuan pinjam lab/alat
    serta menyimpan data pengajuan baru dari mahasiswa.
    """
    # [OTOMATISASI] Memastikan data awal dummy di database RuangLab dan AlatBahan terisi jika masih kosong
    if not RuangLab.objects.exists():
        RuangLab.objects.create(nama_ruang="Lab Atas", kapasitas=30)
        RuangLab.objects.create(nama_ruang="Lab Bawah", kapasitas=30)
        
    if not AlatBahan.objects.exists():
        AlatBahan.objects.create(nama_alat="Stetoskop & Tensimeter")
        AlatBahan.objects.create(nama_alat="Manekin Anatomi Kesehatan")
        AlatBahan.objects.create(nama_alat="Set Bedah Minor / Hecting Kit")

    # Mengecek apakah mahasiswa mengirimkan form (metode POST)
    if request.method == 'POST':
        form = PeminjamanForm(request.POST)
        if form.is_valid():
            # commit=False: Menyiapkan objek data peminjaman tapi jangan disimpan ke DB dulu
            peminjaman = form.save(commit=False)
            
            # Mengisi data otomatis yang tidak ada di dalam pilihan form
            peminjaman.mahasiswa = request.user  # Mengisi peminjam dengan user yang sedang login
            peminjaman.status = 'pending'        # Status awal otomatis 'pending' (menunggu verifikasi ASLAB)
            
            # Simpan data peminjaman secara permanen ke database
            peminjaman.save()
            
            # Tampilkan pesan notifikasi sukses
            messages.success(request, 'Pengajuan peminjaman berhasil dikirim! Menunggu validasi ASLAB.')
            return redirect('mahasiswa:dashboard')
    else:
        # Jika baru pertama kali membuka halaman (metode GET), tampilkan form kosong
        form = PeminjamanForm()
    
    return render(request, 'mahasiswa/form_pinjam.html', {'form': form})


# ==============================================================================
# 3. VIEW FITUR BARU: AJUKAN PENGEMBALIAN LAB/ALAT
# ==============================================================================
@login_required(login_url='core_auth:login')
def ajukan_pengembalian_view(request, pinjam_id):
    """
    Fungsi untuk mengubah status peminjaman menjadi 'pengembalian_diajukan'
    setelah mahasiswa selesai menggunakan laboratorium atau alat.
    """
    # Mengambil objek Peminjaman berdasarkan ID (pinjam_id) dan dipastikan milik user yang login
    peminjaman = get_object_or_404(Peminjaman, id=pinjam_id, mahasiswa=request.user)
    
    # Validasi: Pengembalian hanya boleh diajukan jika status peminjaman saat ini adalah 'disetujui'
    if peminjaman.status == 'disetujui':
        peminjaman.status = 'pengembalian_diajukan'  # Mengubah status di objek
        peminjaman.save()                             # Menyimpan perubahan status ke database
        
        messages.success(request, 'Pengajuan pengembalian berhasil dikirim! Silakan hubungi ASLAB untuk pengecekan alat.')
    else:
        messages.error(request, 'Pengajuan pengembalian tidak dapat diproses untuk status peminjaman ini.')
        
    # Mengarahkan kembali ke halaman dashboard mahasiswa
    return redirect('mahasiswa:dashboard')