# ==============================================================================
# IMPOR MODUL DAN DEPENDENSI DJANGO
# ==============================================================================
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Impor model database yang digunakan dalam aplikasi
from core_auth.models import Peminjaman, RuangLab, AlatBahan

# Impor form HTML bawaan Django
from .forms import PeminjamanForm


# ==============================================================================
# HELPER FUNCTION: PENGECEKAN AUTOMATIS BERDASARKAN USERNAME & GROUP
# ==============================================================================
def cekk_role_mahasiswa(user):
    """
    Fungsi otomatis: Mengecek apakah user yang login BUKAN mahasiswa.
    Mengecek berdasarkan nama username (aslab/kalab), Group, maupun atribut role.
    """
    username_lower = user.username.lower()

    # 1. Cek jika user adalah ASLAB
    if 'aslab' in username_lower or user.groups.filter(name__iexact='ASLAB').exists() or getattr(user, 'role', '').upper() == 'ASLAB':
        return 'aslab:dashboard'

    # 2. Cek jika user adalah KALAB
    if 'kalab' in username_lower or user.groups.filter(name__iexact='KALAB').exists() or getattr(user, 'role', '').upper() == 'KALAB':
        return 'kalab:dashboard'

    return None


# ==============================================================================
# 1. VIEW DASHBOARD MAHASISWA
# ==============================================================================
@login_required(login_url='core_auth:login')
def dashboard_view(request):
    """
    Fungsi untuk menampilkan statistik ringkasan dan daftar riwayat
    peminjaman khusus milik mahasiswa yang sedang login.
    """
    # 🛡️ KEAMANAN AUTOMATIS: Cegah ASLAB / KALAB masuk ke Portal Mahasiswa
    redirect_target = cekk_role_mahasiswa(request.user)
    if redirect_target:
        return redirect(redirect_target)

    # Mengambil semua daftar peminjaman milik user yang login
    jadwal_mahasiswa = Peminjaman.objects.filter(mahasiswa=request.user).order_by('-tanggal_pinjam')
    
    # Menghitung statistik status peminjaman milik user ini
    total_menunggu = Peminjaman.objects.filter(mahasiswa=request.user, status__in=['pending', 'verified']).count()
    total_disetujui = Peminjaman.objects.filter(mahasiswa=request.user, status='disetujui').count()
    total_ditolak = Peminjaman.objects.filter(mahasiswa=request.user, status='ditolak').count()
    
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
    # 🛡️ KEAMANAN AUTOMATIS: Cegah ASLAB / KALAB membuat pengajuan pinjaman
    redirect_target = cekk_role_mahasiswa(request.user)
    if redirect_target:
        return redirect(redirect_target)

    # [OTOMATISASI] Memastikan data awal dummy di database RuangLab dan AlatBahan terisi jika masih kosong
    if not RuangLab.objects.exists():
        RuangLab.objects.create(nama_ruang="Lab Atas", kapasitas=30)
        RuangLab.objects.create(nama_ruang="Lab Bawah", kapasitas=30)
        
    if not AlatBahan.objects.exists():
        AlatBahan.objects.create(nama_alat="Stetoskop & Tensimeter")
        AlatBahan.objects.create(nama_alat="Manekin Anatomi Kesehatan")
        AlatBahan.objects.create(nama_alat="Set Bedah Minor / Hecting Kit")

    if request.method == 'POST':
        form = PeminjamanForm(request.POST)
        if form.is_valid():
            peminjaman = form.save(commit=False)
            peminjaman.mahasiswa = request.user  # Mengisi peminjam dengan user yang sedang login
            peminjaman.status = 'pending'        # Status awal otomatis 'pending' (menunggu verifikasi ASLAB)
            peminjaman.save()
            
            messages.success(request, 'Pengajuan peminjaman berhasil dikirim! Menunggu validasi ASLAB.')
            return redirect('mahasiswa:dashboard')
    else:
        form = PeminjamanForm()
    
    return render(request, 'mahasiswa/form_pinjam.html', {'form': form})


# ==============================================================================
# 3. VIEW FITUR: AJUKAN PENGEMBALIAN LAB/ALAT
# ==============================================================================
@login_required(login_url='core_auth:login')
def ajukan_pengembalian_view(request, pinjam_id):
    """
    Fungsi untuk mengubah status peminjaman menjadi 'pengembalian_diajukan'
    setelah mahasiswa selesai menggunakan laboratorium atau alat.
    """
    # 🛡️ KEAMANAN AUTOMATIS: Cegah ASLAB / KALAB memproses URL ini
    redirect_target = cekk_role_mahasiswa(request.user)
    if redirect_target:
        return redirect(redirect_target)

    # Mengambil objek Peminjaman berdasarkan ID dan dipastikan milik mahasiswa yang sedang login
    peminjaman = get_object_or_404(Peminjaman, id=pinjam_id, mahasiswa=request.user)
    
    if peminjaman.status == 'disetujui':
        peminjaman.status = 'pengembalian_diajukan'
        peminjaman.save()
        messages.success(request, 'Pengajuan pengembalian berhasil dikirim! Silakan hubungi ASLAB untuk pengecekan alat.')
    else:
        messages.error(request, 'Pengajuan pengembalian tidak dapat diproses untuk status peminjaman ini.')
        
    return redirect('mahasiswa:dashboard')